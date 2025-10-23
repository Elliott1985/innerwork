# InnerWork - Self-Paced Therapy & Psychoeducation Platform

A Flask-based web application designed for **Debbie Green, MA, PSC** of **Journeys Edgez Life Coaching**. InnerWork provides a self-paced learning platform with therapy modules, AI chatbot support, quizzes, certificates, and payment integration.

## 🌟 Features

- **User Authentication**: Secure registration and login system
- **Module System**: Video-based learning modules with embedded content
- **Interactive Quizzes**: Test knowledge with multiple-choice assessments
- **Progress Tracking**: Monitor completion status and scores
- **Certificate Generation**: PDF certificates upon module completion
- **Virtual Therapist**: AI-powered chatbot for support and guidance (placeholder for OpenAI integration)
- **Payment Integration**: Stripe integration for module purchases (test mode included)
- **Responsive Design**: Beautiful, mobile-friendly interface with warm color palette

## 🎨 Design

- **Color Palette**: Lavender, rose, rose-gold, and beige tones
- **Typography**: Inter font family
- **Framework**: Bootstrap 5 with custom CSS

## 🛠️ Technology Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **PDF Generation**: ReportLab
- **Payments**: Stripe
- **Frontend**: Bootstrap 5, Vanilla JavaScript

## 📁 Project Structure

```
innerwork/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (gitignored)
├── .env.example           # Environment variables template
├── routes/
│   ├── auth.py            # Authentication routes
│   ├── modules.py         # Module and quiz routes
│   ├── chatbot.py         # Chatbot routes
│   └── payments.py        # Payment routes
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # User dashboard
│   ├── module.html        # Module view and list
│   ├── chatbot.html       # Chatbot interface
│   └── checkout.html      # Payment checkout
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   └── chatbot.js     # Chatbot functionality
│   └── images/            # Static images
└── db/
    └── innerwork.db       # SQLite database (auto-created)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project**:
   ```bash
   cd /path/to/innerwork
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your actual keys:
   - `FLASK_SECRET_KEY`: Generate a secure random key
   - `STRIPE_API_KEY`: Your Stripe test API key
   - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key
   - `OPENAI_API_KEY`: Your OpenAI API key (for future chatbot integration)

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

## 📝 Usage

### Initial Setup

1. **Register a new account** at `/register`
2. **Login** with your credentials
3. **Browse modules** from the dashboard
4. **Purchase a module** (test mode - auto-completes)
5. **Complete quizzes** to earn certificates
6. **Chat with Virtual Debbie** for support

### Admin Tasks

To add modules to the database, you can use Python shell:

```python
from app import create_app
from models import db, Module
import json

app = create_app()
with app.app_context():
    quiz = [
        {
            "question": "What is mindfulness?",
            "options": ["Being present", "Being busy", "Being stressed", "Being tired"],
            "correct_answer": "Being present"
        }
    ]
    
    module = Module(
        title="Introduction to Mindfulness",
        description="Learn the basics of mindfulness practice",
        video_url="https://www.youtube.com/embed/example",
        quiz_questions=json.dumps(quiz)
    )
    
    db.session.add(module)
    db.session.commit()
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Flask session secret key | dev-secret-key |
| `STRIPE_API_KEY` | Stripe secret API key | sk_test_placeholder |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | pk_test_placeholder |
| `OPENAI_API_KEY` | OpenAI API key | sk-placeholder |
| `DATABASE_URL` | Database connection string | sqlite:///db/innerwork.db |
| `FLASK_ENV` | Flask environment | development |

## 🧪 Testing

The application runs in test mode by default:
- Payments are simulated (no actual charges)
- Chatbot uses placeholder responses
- Database is SQLite (file-based)

## 🔐 Security Notes

- Never commit `.env` file to version control
- Change default secret keys in production
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Add CSRF protection for forms
- Validate and sanitize all user inputs

## 🚀 Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production-grade database (PostgreSQL recommended)
3. Configure a production WSGI server (Gunicorn, uWSGI)
4. Set up reverse proxy (Nginx, Apache)
5. Enable SSL/TLS certificates
6. Configure real Stripe keys
7. Integrate OpenAI API for chatbot
8. Set up monitoring and logging

## 📄 License

This project is proprietary software for Journeys Edgez Life Coaching.

## 👤 Contact

**Debbie Green, MA, PSC**  
Journeys Edgez Life Coaching

---

## 🔮 Future Enhancements

- [ ] OpenAI integration for Virtual Debbie
- [ ] Email notifications for course completion
- [ ] Progress analytics dashboard
- [ ] Multiple quiz attempts
- [ ] Video upload functionality
- [ ] Social sharing features
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Subscription plans
- [ ] Community forums

---

Built with ❤️ for mental health and wellness education.
