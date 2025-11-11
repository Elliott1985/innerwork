import os
from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from models import db, ChatHistory
from datetime import datetime
from openai import OpenAI

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# System prompt defining Debbie Green's therapeutic persona
SYSTEM_PROMPT = """You are Debbie Green, MA, PSC — a compassionate psychotherapist and life coach with Journeys Edgez Life Coaching.

Your communication style:
- Warm, empathetic, and trauma-sensitive
- Clinical but conversational — you balance professional insight with accessible language
- Use reflective listening: acknowledge feelings, validate experiences
- Ask gentle, open-ended questions to encourage self-exploration
- Offer psychoeducation when appropriate (explain concepts clearly)
- Emphasize strengths, resilience, and growth potential
- Create a safe, non-judgmental space
- Use "I" statements when sharing perspectives ("I notice...", "I wonder if...")
- Keep responses concise but meaningful (2-4 sentences typically)
- Respect boundaries — if someone needs crisis support, gently encourage professional help

Your specialties: mindfulness, emotional regulation, self-compassion, life transitions, personal growth.

Remember: You're a supportive guide, not a replacement for in-person therapy. Build trust through consistency, empathy, and authentic presence."""

def get_conversation_history():
    """Retrieve conversation history from session (max 6 turns = 12 messages)"""
    if 'conversation' not in session:
        session['conversation'] = []
    return session['conversation']

def save_conversation_turn(user_message, assistant_message):
    """Save a conversation turn to session, maintaining max 6 turns"""
    conversation = get_conversation_history()
    conversation.append({"role": "user", "content": user_message})
    conversation.append({"role": "assistant", "content": assistant_message})
    
    # Keep only last 6 turns (12 messages: 6 user + 6 assistant)
    if len(conversation) > 12:
        conversation = conversation[-12:]
    
    session['conversation'] = conversation
    session.modified = True

def get_openai_response(user_message):
    """Get response from OpenAI with conversation context"""
    try:
        # Build messages for API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        conversation = get_conversation_history()
        messages.extend(conversation)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=os.getenv('MODEL_NAME', 'gpt-4o-mini'),
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm having trouble connecting right now. Please try again in a moment. If this persists, please reach out for support."

@chatbot_bp.route('/chatbot')
@login_required
def chatbot_page():
    # Get recent chat history for this user from database
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
    
    # Get AI response with conversation context
    response = get_openai_response(user_input)
    
    # Save conversation turn to session
    save_conversation_turn(user_input, response)
    
    # Save to database for persistence
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

@chatbot_bp.route('/chatbot/clear', methods=['POST'])
@login_required
def clear_conversation():
    """Clear current conversation session"""
    session['conversation'] = []
    session.modified = True
    return jsonify({"status": "success", "message": "Conversation cleared"})

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
