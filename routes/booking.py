from flask import Blueprint, render_template
from flask_login import login_required

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book')
@login_required
def book():
    """Show Calendly booking page for 1:1 sessions."""
    return render_template('book.html')
