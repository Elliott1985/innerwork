from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models import db, Enrollment, Module

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Show user's enrolled modules with progress."""
    enrollments = (db.session.query(Enrollment, Module)
                   .join(Module, Enrollment.module_id == Module.id)
                   .filter(Enrollment.user_id == current_user.id)
                   .all())
    return render_template('dashboard/index.html', progress=enrollments)

@dashboard_bp.route('/progress/<int:module_id>/<int:new_percent>', methods=['POST'])
@login_required
def update_progress(module_id, new_percent):
    """Update progress for a module."""
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id, 
        module_id=module_id
    ).first_or_404()
    
    enrollment.progress = max(0, min(100, new_percent))
    if enrollment.progress >= 100:
        enrollment.status = 'complete'
    
    db.session.commit()
    return jsonify({
        'ok': True, 
        'progress': enrollment.progress, 
        'status': enrollment.status
    })
