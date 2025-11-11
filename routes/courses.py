from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Purchase, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

# Sample course data showcasing self-paced programs
courses_data = [
    {
        "id": 1,
        "title": "I Am Not My Trauma",
        "description": "Learn to separate identity from experience through guided reflection and self-paced exercises. This transformative journey helps you reclaim your sense of self beyond past experiences.",
        "duration": "4 Modules",
        "level": "Beginner",
        "tag": "Emotional Healing",
        "price": "$49.99",
        "price_cents": 4999,
        "features": [
            "4 video modules with guided exercises",
            "Interactive journaling prompts",
            "Completion certificate",
            "Lifetime access"
        ]
    },
    {
        "id": 2,
        "title": "I'm Sorry Is No Longer an Option",
        "description": "A boundary-building journey toward emotional strength and personal clarity. Learn to honor your needs without apology and cultivate healthy relationship dynamics.",
        "duration": "6 Modules",
        "level": "Intermediate",
        "tag": "Boundaries",
        "price": "$79.99",
        "price_cents": 7999,
        "features": [
            "6 comprehensive video lessons",
            "Boundary-setting workbook",
            "Role-play scenarios and scripts",
            "Certificate of completion"
        ]
    },
    {
        "id": 3,
        "title": "Heart & Mind Connection",
        "description": "Explore the spiritual and psychological connection between emotion and thought. Discover practices for integrating mind-body awareness into daily life.",
        "duration": "5 Modules",
        "level": "Advanced",
        "tag": "Mindfulness",
        "price": "$69.99",
        "price_cents": 6999,
        "features": [
            "5 deep-dive video modules",
            "Guided meditation practices",
            "Mind-body integration exercises",
            "Digital certificate"
        ]
    },
    {
        "id": 4,
        "title": "Navigating Grief with Grace",
        "description": "A compassionate guide through the stages of grief and loss. Learn healthy coping mechanisms and honor your healing process with self-compassion.",
        "duration": "8 Modules",
        "level": "All Levels",
        "tag": "Grief & Loss",
        "price": "$89.99",
        "price_cents": 8999,
        "features": [
            "8 gentle, paced video lessons",
            "Grief journal templates",
            "Community support access",
            "Completion certificate"
        ]
    }
]

@courses_bp.route('/')
def list_courses():
    """Display all available courses in the library"""
    # Check which courses user has purchased (if authenticated)
    purchased_ids = []
    if current_user.is_authenticated:
        purchases = Purchase.query.filter_by(
            user_id=current_user.id,
            payment_status='completed'
        ).all()
        purchased_ids = [p.module_id for p in purchases]
    
    return render_template('courses/index.html', 
                         courses=courses_data,
                         purchased_ids=purchased_ids)

@courses_bp.route('/<int:course_id>')
def course_detail(course_id):
    """Display detailed information about a specific course"""
    course = next((c for c in courses_data if c["id"] == course_id), None)
    
    if not course:
        return render_template('404.html'), 404
    
    # Check if user has purchased this course (check both Purchase and Enrollment tables)
    is_purchased = False
    if current_user.is_authenticated:
        # Check old Purchase table
        purchase = Purchase.query.filter_by(
            user_id=current_user.id,
            module_id=course_id,
            payment_status='completed'
        ).first()
        # Check new Enrollment table
        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id,
            module_id=course_id
        ).first()
        is_purchased = bool(purchase or enrollment)
    
    return render_template('courses/detail.html', 
                         course=course,
                         is_purchased=is_purchased)
