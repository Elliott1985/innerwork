import os
import stripe
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Module, Purchase
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_API_KEY')

@payments_bp.route('/checkout/<int:module_id>')
@login_required
def checkout(module_id):
    module = Module.query.get_or_404(module_id)
    
    # Check if already purchased
    existing_purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        module_id=module_id,
        payment_status='completed'
    ).first()
    
    if existing_purchase:
        flash('You already own this module!', 'info')
        return redirect(url_for('modules.view_module', module_id=module_id))
    
    stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    
    return render_template('checkout.html', 
                         module=module, 
                         stripe_publishable_key=stripe_publishable_key)

@payments_bp.route('/create-checkout-session/<int:module_id>', methods=['POST'])
@login_required
def create_checkout_session(module_id):
    module = Module.query.get_or_404(module_id)
    
    try:
        # For now, this is a placeholder - in production, you'll create a real Stripe session
        # Simulating a purchase for development
        
        # Create purchase record
        purchase = Purchase(
            user_id=current_user.id,
            module_id=module_id,
            plan_type='one-time',
            payment_status='completed',  # In dev mode, auto-complete
            stripe_payment_id='test_payment_' + str(datetime.utcnow().timestamp())
        )
        db.session.add(purchase)
        db.session.commit()
        
        flash('Purchase successful! (Test mode)', 'success')
        return jsonify({'redirect': url_for('modules.view_module', module_id=module_id)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """
    Stripe webhook endpoint to handle payment events.
    In production, this will process real Stripe webhook events.
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    # Placeholder for webhook handling
    # In production, verify signature and process events like:
    # - checkout.session.completed
    # - payment_intent.succeeded
    # - payment_intent.payment_failed
    
    return jsonify({'status': 'success'}), 200

@payments_bp.route('/pricing')
def pricing():
    """Display pricing information for all modules"""
    modules = Module.query.all()
    return render_template('pricing.html', modules=modules)
