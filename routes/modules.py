import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models import db, Module, Progress, Purchase, Enrollment
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

modules_bp = Blueprint('modules', __name__)

@modules_bp.route('/dashboard')
@login_required
def dashboard():
    # Import hardcoded course data
    from routes.courses import courses_data
    
    # Get user's progress (old system)
    user_progress = Progress.query.filter_by(user_id=current_user.id).all()
    
    # Get purchased modules from old Purchase table
    purchases = Purchase.query.filter_by(
        user_id=current_user.id, 
        payment_status='completed'
    ).all()
    purchased_module_ids = [p.module_id for p in purchases]
    
    # Get enrolled modules from new Enrollment table (Stripe purchases)
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    enrolled_module_ids = [e.module_id for e in enrollments]
    
    # Combine both sources
    all_module_ids = list(set(purchased_module_ids + enrolled_module_ids))
    
    # Get modules from database if they exist, otherwise use hardcoded data
    db_modules = Module.query.filter(Module.id.in_(all_module_ids)).all() if all_module_ids else []
    
    # Convert hardcoded courses to module-like objects for enrolled courses
    available_modules = []
    if db_modules:
        available_modules = db_modules
    else:
        # Use hardcoded course data for enrolled courses
        for module_id in all_module_ids:
            course = next((c for c in courses_data if c['id'] == module_id), None)
            if course:
                # Create a simple object with course data
                class CourseModule:
                    def __init__(self, course_dict):
                        self.id = course_dict['id']
                        self.title = course_dict['title']
                        self.description = course_dict['description']
                available_modules.append(CourseModule(course))
    
    # Create progress map (prefer new Enrollment progress over old Progress)
    progress_map = {p.module_id: p for p in user_progress}
    
    # Add enrollment progress data (convert to match old Progress format for template compatibility)
    for enrollment in enrollments:
        if enrollment.module_id not in progress_map:
            # Create a pseudo-Progress object for template compatibility
            class EnrollmentProgress:
                def __init__(self, enrollment):
                    self.module_id = enrollment.module_id
                    self.score = enrollment.progress
                    self.completed_date = enrollment.created_at
            progress_map[enrollment.module_id] = EnrollmentProgress(enrollment)
    
    return render_template('dashboard.html', 
                         modules=available_modules, 
                         progress_map=progress_map)

@modules_bp.route('/modules')
@login_required
def list_modules():
    all_modules = Module.query.all()
    
    # Get user's purchases
    purchases = Purchase.query.filter_by(
        user_id=current_user.id, 
        payment_status='completed'
    ).all()
    purchased_ids = [p.module_id for p in purchases]
    
    return render_template('module.html', 
                         modules=all_modules, 
                         purchased_ids=purchased_ids)

@modules_bp.route('/module/<int:module_id>')
@login_required
def view_module(module_id):
    module = Module.query.get_or_404(module_id)
    
    # Check if user has purchased this module
    purchase = Purchase.query.filter_by(
        user_id=current_user.id, 
        module_id=module_id,
        payment_status='completed'
    ).first()
    
    if not purchase:
        flash('You need to purchase this module first.', 'warning')
        return redirect(url_for('payments.checkout', module_id=module_id))
    
    # Parse quiz questions
    quiz_questions = json.loads(module.quiz_questions) if module.quiz_questions else []
    
    # Check if user has completed this module
    progress = Progress.query.filter_by(
        user_id=current_user.id, 
        module_id=module_id
    ).first()
    
    return render_template('module.html', 
                         module=module, 
                         quiz_questions=quiz_questions,
                         progress=progress)

@modules_bp.route('/module/<int:module_id>/submit-quiz', methods=['POST'])
@login_required
def submit_quiz(module_id):
    module = Module.query.get_or_404(module_id)
    
    # Get quiz answers from form
    quiz_questions = json.loads(module.quiz_questions) if module.quiz_questions else []
    
    if not quiz_questions:
        flash('No quiz available for this module.', 'warning')
        return redirect(url_for('modules.view_module', module_id=module_id))
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz_questions)
    
    for i, question in enumerate(quiz_questions):
        user_answer = request.form.get(f'question_{i}')
        if user_answer and user_answer == question.get('correct_answer'):
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    
    # Save or update progress
    progress = Progress.query.filter_by(
        user_id=current_user.id, 
        module_id=module_id
    ).first()
    
    if progress:
        progress.score = score
        progress.completed_date = datetime.utcnow()
    else:
        progress = Progress(
            user_id=current_user.id,
            module_id=module_id,
            score=score
        )
        db.session.add(progress)
    
    db.session.commit()
    
    flash(f'Quiz submitted! Your score: {score}%', 'success')
    return redirect(url_for('modules.view_module', module_id=module_id))

@modules_bp.route('/certificate/<int:module_id>')
@login_required
def download_certificate(module_id):
    module = Module.query.get_or_404(module_id)
    progress = Progress.query.filter_by(
        user_id=current_user.id, 
        module_id=module_id
    ).first()
    
    if not progress:
        flash('You need to complete this module first.', 'warning')
        return redirect(url_for('modules.view_module', module_id=module_id))
    
    # Generate PDF certificate
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Certificate design
    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width / 2, height - 100, "Certificate of Completion")
    
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2, height - 200, "This certifies that")
    
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 250, current_user.name)
    
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2, height - 320, "has successfully completed")
    
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 370, module.title)
    
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, height - 440, f"Score: {progress.score}%")
    p.drawCentredString(width / 2, height - 470, f"Date: {progress.completed_date.strftime('%B %d, %Y')}")
    
    p.setFont("Helvetica-Oblique", 12)
    p.drawCentredString(width / 2, 100, "Journeys Edgez Life Coaching - Debbie Green, MA, PSC")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, 
                     as_attachment=True,
                     download_name=f'certificate_{module.title.replace(" ", "_")}.pdf',
                     mimetype='application/pdf')
