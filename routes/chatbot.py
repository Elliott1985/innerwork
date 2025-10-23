import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, ChatHistory
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot')
@login_required
def chatbot_page():
    # Get recent chat history for this user
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.desc()).limit(20).all()
    chat_history.reverse()  # Show oldest first
    return render_template('chatbot.html', chat_history=chat_history)

@chatbot_bp.route('/chatbot/message', methods=['POST'])
@login_required
def chatbot_reply():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # Placeholder response (will be replaced with OpenAI integration later)
    response = f"Virtual Debbie says: I hear you. Let's take a deep breath and think about that. You mentioned: '{user_input[:50]}...' - I'm here to support you on your journey."
    
    # Save to chat history
    chat_entry = ChatHistory(
        user_id=current_user.id,
        message=user_input,
        response=response,
        timestamp=datetime.utcnow()
    )
    db.session.add(chat_entry)
    db.session.commit()
    
    return jsonify({
        "response": response,
        "timestamp": chat_entry.timestamp.isoformat()
    })

@chatbot_bp.route('/chatbot/history')
@login_required
def get_chat_history():
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.asc()).all()
    
    history_data = [
        {
            "message": chat.message,
            "response": chat.response,
            "timestamp": chat.timestamp.isoformat()
        }
        for chat in chat_history
    ]
    
    return jsonify({"history": history_data})
