import os
import stripe
from flask import Blueprint, request, jsonify, url_for, redirect, flash, current_app
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from models import db, Module, Enrollment

stripe_bp = Blueprint('stripe', __name__, url_prefix='/stripe')

# Test mode flag - set to True to bypass Stripe
TEST_MODE = True

def send_email_safe(to, subject, html):
    """Send email with console fallback if SMTP not configured."""
    try:
        mail = Mail(current_app)
        if not current_app.config.get('MAIL_SERVER') or not current_app.config.get('MAIL_USERNAME'):
            print("\n--- EMAIL (console fallback) ---")
            print("To:", to)
            print("Subject:", subject)
            print(html)
            print("--- END EMAIL ---\n")
            return True
        
        msg = Message(subject, recipients=[to], html=html)
        mail.send(msg)
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False

@stripe_bp.route('/purchase/<int:module_id>', methods=['POST'])
@login_required
def purchase_module(module_id):
    """Create Stripe checkout session for module purchase."""
    # Import hardcoded course data
    from routes.courses import courses_data
    course = next((c for c in courses_data if c["id"] == module_id), None)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # TEST MODE: Skip Stripe and directly enroll
    if TEST_MODE:
        # Check if already enrolled
        existing = Enrollment.query.filter_by(
            user_id=current_user.id,
            module_id=module_id
        ).first()
        
        if not existing:
            enrollment = Enrollment(
                user_id=current_user.id,
                module_id=module_id,
                progress=0,
                status='in_progress'
            )
            db.session.add(enrollment)
            db.session.commit()
        
        # Send test email
        send_email_safe(
            to=current_user.email,
            subject=f'InnerWork: Test Enrollment - {course["title"]}',
            html=f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #6a5acd;">Test Enrollment Confirmed!</h2>
                    <p>Hi {current_user.name},</p>
                    <p>This is a test enrollment. Your access to <strong>{course['title']}</strong> is now active.</p>
                    <p>You can continue your module anytime from your dashboard.</p>
                    <p style="margin-top: 30px;">
                        <a href="{url_for('modules.dashboard', _external=True)}" 
                           style="background: #6a5acd; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Go to Dashboard
                        </a>
                    </p>
                    <p style="color: #666; margin-top: 30px; font-size: 14px;">— InnerWork Team (TEST MODE)</p>
                </div>
            """
        )
        
        return jsonify({
            'test_mode': True,
            'redirect': url_for('modules.dashboard')
        })
    
    try:
        checkout_session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': course['price_cents'],
                    'product_data': {
                        'name': f'InnerWork Module – {course["title"]}',
                        'description': course['description'],
                    },
                },
                'quantity': 1,
            }],
            success_url=url_for('stripe.purchase_success', module_id=module_id, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('courses.course_detail', course_id=module_id, _external=True),
            customer_email=current_user.email,
            metadata={
                'module_id': str(module_id),
                'user_id': str(current_user.id),
                'user_email': current_user.email,
            },
        )
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@stripe_bp.route('/purchase/success/<int:module_id>')
@login_required
def purchase_success(module_id):
    """Handle successful purchase, create enrollment, send email."""
    session_id = request.args.get('session_id')
    
    # Verify session with Stripe (optional but recommended)
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status != 'paid':
                flash('Payment not completed. Please try again.', 'warning')
                return redirect(url_for('courses.course_detail', course_id=module_id))
        except Exception as e:
            print("Stripe verification failed:", e)
    
    # Create or update enrollment
    existing = Enrollment.query.filter_by(
        user_id=current_user.id, 
        module_id=module_id
    ).first()
    
    if not existing:
        enrollment = Enrollment(
            user_id=current_user.id,
            module_id=module_id,
            progress=0,
            status='in_progress'
        )
        db.session.add(enrollment)
        db.session.commit()
    
    # Send confirmation email
    from routes.courses import courses_data
    course = next((c for c in courses_data if c["id"] == module_id), None)
    course_title = course['title'] if course else 'Course'
    send_email_safe(
        to=current_user.email,
        subject=f'InnerWork: Purchase Confirmed – {course_title}',
        html=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #6a5acd;">Purchase Confirmed!</h2>
                <p>Hi {current_user.name},</p>
                <p>Thanks for your purchase! Your access to <strong>{course_title}</strong> is now active.</p>
                <p>You can continue your module anytime from your dashboard.</p>
                <p style="margin-top: 30px;">
                    <a href="{url_for('modules.dashboard', _external=True)}" 
                       style="background: #6a5acd; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                        Go to Dashboard
                    </a>
                </p>
                <p style="color: #666; margin-top: 30px; font-size: 14px;">— InnerWork Team</p>
            </div>
        """
    )
    
    flash('Purchase confirmed! We emailed your receipt and unlocked the module in your dashboard.', 'success')
    return redirect(url_for('modules.dashboard'))
