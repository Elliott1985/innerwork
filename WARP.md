# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

InnerWork is a Flask-based self-paced therapy & psychoeducation platform for Journeys Edgez Life Coaching. The application provides video-based learning modules with quizzes, AI chatbot support, certificate generation, and Stripe payment integration.

**Client**: Debbie Green, MA, PSC  
**Design**: Lavender, rose, rose-gold, and beige color palette with Inter font

## Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy .env.example to .env first)
cp .env.example .env
```

### Running the Application
```bash
# Run development server (debug mode, port 5000)
python app.py
```

### Database Management
```bash
# Access Python shell with app context
python -c "from app import create_app; app = create_app(); app.app_context().push()"

# Add a module (run in Python shell):
from models import db, Module
import json

quiz = [{"question": "...", "options": [...], "correct_answer": "..."}]
module = Module(title="...", description="...", video_url="...", quiz_questions=json.dumps(quiz))
db.session.add(module)
db.session.commit()
```

## Architecture

### Core Structure

**Blueprint-Based Organization**: The application uses Flask blueprints for modular route organization:
- `routes/auth.py` - User registration, login, logout (Flask-Login)
- `routes/modules.py` - Module viewing, quiz submission, certificate generation (ReportLab PDF)
- `routes/chatbot.py` - OpenAI-powered therapeutic chatbot with session-aware conversation memory
- `routes/payments.py` - Stripe payment integration (test mode by default)

**Database Models** (SQLAlchemy ORM):
- `User` - Authentication with password hashing (Werkzeug), relationships to Progress, Purchase, ChatHistory
- `Module` - Learning modules with video URLs and JSON-stored quiz questions
- `Progress` - User completion tracking with scores and dates
- `Purchase` - Payment records with Stripe integration (plan_type: one-time/monthly/yearly)
- `ChatHistory` - Persistent chat logs for Virtual Debbie

### Key Technical Patterns

**Authentication Flow**: Flask-Login manages sessions; `@login_required` decorator protects routes; unauthorized users redirect to login with `next` parameter support.

**Module Access Control**: Users must have a completed Purchase record (`payment_status='completed'`) to access module content. Access checks occur in `view_module()` route.

**Quiz System**: Questions stored as JSON strings in `Module.quiz_questions`. Form submission calculates percentage score, creates/updates Progress record, triggers certificate availability.

**Certificate Generation**: ReportLab generates PDF certificates on-the-fly with user name, module title, score, completion date. Uses BytesIO for in-memory file handling.

**Payment Integration**: Currently in test mode (auto-completes purchases). Production requires real Stripe API keys and webhook implementation for events like `checkout.session.completed`.

**Chatbot System**: OpenAI-powered conversational AI using `gpt-4o-mini` model. Maintains conversation context in Flask sessions (up to 6 turns = 12 messages). System prompt defines Debbie Green's therapeutic persona: warm, empathetic, trauma-sensitive, clinical-conversational tone. Responses stored in database (ChatHistory) for persistence; session stores working memory. Clear session endpoint resets conversation context.

### Environment Variables

Critical configuration in `.env`:
- `FLASK_SECRET_KEY` - Session security (must be random in production)
- `STRIPE_API_KEY` / `STRIPE_PUBLISHABLE_KEY` - Payment integration
- `OPENAI_API_KEY` - **Required** for chatbot functionality (OpenAI API key)
- `MODEL_NAME` - OpenAI model to use (default: `gpt-4o-mini`)
- `DATABASE_URL` - Defaults to SQLite at `sqlite:///db/innerwork.db`
- `FLASK_ENV` - Set to `production` for deployment

### Frontend Integration

- Templates in `templates/` extend `base.html` with Bootstrap 5
- Custom styles in `static/css/style.css` (lavender/rose/beige theme)
- Chatbot JavaScript in `static/js/chatbot.js` handles AJAX message sending
- Stripe checkout requires publishable key passed to templates

## Development Notes

- **Database**: SQLite for development; migrate to PostgreSQL for production
- **Payments**: Test mode auto-completes purchases; implement real Stripe checkout sessions and webhook verification for production
- **Chatbot**: Fully functional with OpenAI integration; requires valid `OPENAI_API_KEY` in `.env`; conversation context stored in Flask sessions (filesystem-based)
- **Session Storage**: Flask-Session uses filesystem storage in `flask_session/` directory (gitignored); consider Redis for production
- **Security**: Never commit `.env`; use HTTPS in production; implement CSRF protection and rate limiting
- **Deployment**: Use Gunicorn/uWSGI with Nginx; enable SSL/TLS; set `FLASK_ENV=production`

## Module JSON Format

Quiz questions must follow this structure:
```json
[
  {
    "question": "Question text?",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer": "Option 1"
  }
]
```

Store as JSON string in `Module.quiz_questions` using `json.dumps()`.
