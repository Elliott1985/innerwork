# Virtual Debbie Chatbot - Setup & Usage Guide

## 🌟 Overview

The Virtual Debbie chatbot is a fully functional, session-aware conversational AI therapist powered by OpenAI's GPT-4o-mini. It embodies the compassionate, trauma-sensitive approach of Debbie Green, MA, PSC from Journeys Edgez Life Coaching.

## ✨ Features

- **Session-Aware Conversations**: Maintains context for up to 6 conversation turns
- **Therapeutic Persona**: Warm, empathetic, clinical yet conversational tone
- **Persistent Storage**: All conversations saved to database for user history
- **Beautiful UI**: Trauma-sensitive design with lavender, rose gold, and beige aesthetics
- **Real-time Chat**: AJAX-based messaging with typing indicators
- **Session Management**: Clear conversation context to start fresh

## 🔧 Setup Instructions

### 1. Install Dependencies

The required packages are already in `requirements.txt`:

```bash
./venv/bin/pip install -r requirements.txt
```

This installs:
- `openai==1.12.0` - OpenAI Python SDK
- `Flask-Session==0.5.0` - Session management

### 2. Configure OpenAI API Key

**Get your OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-...`)

**Update `.env` file:**

```bash
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
MODEL_NAME=gpt-4o-mini
```

⚠️ **Important**: Never commit your `.env` file to version control!

### 3. Run the Application

```bash
./venv/bin/python app.py
```

The app runs on http://localhost:5001

## 📖 Usage

### Accessing the Chatbot

1. Register/login to your account
2. Navigate to `/chatbot` or click "Virtual Debbie" in the navigation
3. Start chatting!

### Conversation Features

- **Context Memory**: The chatbot remembers the last 6 exchanges (12 messages)
- **Clear Session**: Click "Clear" button to reset conversation context
- **History**: All messages are saved to database for future reference
- **Message Counter**: See how many messages in current session

### Example Interactions

**User**: "I've been feeling overwhelmed lately with work stress."

**Virtual Debbie**: "I hear you, and it sounds like work has been weighing heavily on you. Feeling overwhelmed is a common response when we're carrying a lot. What aspect of the work stress feels most pressing for you right now?"

## 🎨 Design Philosophy

The chatbot UI follows trauma-sensitive design principles:

- **Soft Color Palette**: Lavender (#c59fc9), Rose (#d4a5a5), Beige (#f8f5f2)
- **Calm Animations**: Gentle fade-in effects
- **Clear Typography**: Easy-to-read Inter font
- **Safe Messaging**: Crisis support information prominently displayed
- **Non-threatening Layout**: Spacious, breathing room in design

## 🏗️ Architecture

### Backend (`routes/chatbot.py`)

```python
# Key Components:
- SYSTEM_PROMPT: Defines Debbie's therapeutic persona
- get_conversation_history(): Retrieves last 6 turns from Flask session
- save_conversation_turn(): Saves messages and maintains 6-turn limit
- get_openai_response(): Calls OpenAI API with full context
```

### Frontend (`static/js/chatbot.js`)

```javascript
// Key Features:
- Real-time message rendering with avatars
- Typing indicators during API calls
- Auto-scroll to latest message
- Message count tracking
- Session clearing functionality
```

### Session Management

- **Type**: Filesystem-based (Flask-Session)
- **Location**: `flask_session/` directory (gitignored)
- **Persistence**: Until browser session ends or manual clear
- **Limit**: 6 conversation turns (12 messages)

## 🔒 Security & Privacy

### Data Storage

- **Session Data**: Stored locally in `flask_session/` directory
- **Database**: All conversations saved to `ChatHistory` table
- **User Isolation**: Each user only sees their own history

### API Key Security

- Never expose OpenAI API key in client-side code
- All API calls happen server-side
- Use environment variables for configuration

### Rate Limiting (TODO)

Consider implementing:
- Message rate limiting per user
- API call throttling
- Cost monitoring for OpenAI usage

## 💰 Cost Considerations

### OpenAI Pricing (as of 2024)

GPT-4o-mini:
- Input: $0.150 per 1M tokens
- Output: $0.600 per 1M tokens

### Estimated Costs

Typical conversation (6 turns):
- System prompt: ~200 tokens
- User messages: ~50 tokens each = 300 tokens
- Assistant responses: ~100 tokens each = 600 tokens
- Context overhead: ~300 tokens
- **Total per conversation**: ~1,400 tokens ≈ $0.001

For 1,000 users having 10 conversations/month:
- 10,000 conversations × $0.001 = **$10/month**

## 🚀 Production Considerations

### Recommended Upgrades

1. **Session Storage**: Switch from filesystem to Redis
   ```python
   app.config['SESSION_TYPE'] = 'redis'
   app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
   ```

2. **Rate Limiting**: Add Flask-Limiter
   ```python
   @limiter.limit("10 per minute")
   @chatbot_bp.route('/chatbot/message', methods=['POST'])
   ```

3. **Error Handling**: Implement retry logic for API failures
4. **Monitoring**: Track API usage and costs
5. **Streaming**: Consider streaming responses for better UX
6. **Content Filtering**: Add OpenAI moderation endpoint

### Environment Variables for Production

```bash
FLASK_ENV=production
FLASK_SECRET_KEY=<strong-random-key>
OPENAI_API_KEY=<production-key>
MODEL_NAME=gpt-4o-mini
SESSION_TYPE=redis
REDIS_URL=redis://localhost:6379
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] New conversation starts properly
- [ ] Context maintained across 6 turns
- [ ] Clear session resets conversation
- [ ] Messages saved to database
- [ ] Typing indicator appears/disappears
- [ ] Error handling works (invalid API key, network issues)
- [ ] UI displays correctly on mobile
- [ ] Crisis information visible

### Testing Without API Key

If you need to test without spending OpenAI credits, modify `routes/chatbot.py`:

```python
def get_openai_response(user_message):
    # Mock response for testing
    return f"[TEST MODE] I hear you saying: {user_message[:50]}..."
```

## 📝 Customization

### Adjusting Conversation Memory

Change the turn limit in `routes/chatbot.py`:

```python
def save_conversation_turn(user_message, assistant_message):
    # ...
    # Keep only last 10 turns (20 messages) instead of 6
    if len(conversation) > 20:
        conversation = conversation[-20:]
```

### Modifying Therapist Persona

Edit `SYSTEM_PROMPT` in `routes/chatbot.py` to adjust:
- Tone and style
- Specialties
- Response length
- Therapeutic approach

### Changing Model

Update `.env` to use different OpenAI models:
```bash
# More capable but slower/expensive
MODEL_NAME=gpt-4-turbo

# Faster but less nuanced
MODEL_NAME=gpt-3.5-turbo
```

## 🐛 Troubleshooting

### "OpenAI API Error"

**Cause**: Invalid or missing API key
**Solution**: Check `.env` file has valid `OPENAI_API_KEY`

### Sessions Not Persisting

**Cause**: `flask_session/` directory missing or not writable
**Solution**: `mkdir -p flask_session && chmod 755 flask_session`

### High API Costs

**Cause**: Too many conversation turns retained
**Solution**: Reduce turn limit from 6 to 3-4

### Slow Responses

**Cause**: Large context or model selection
**Solution**: 
- Reduce `max_tokens` in API call
- Use `gpt-3.5-turbo` instead of `gpt-4o-mini`
- Implement streaming responses

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask-Session Documentation](https://flask-session.readthedocs.io/)
- [Trauma-Informed Design Principles](https://www.traumainformeddesign.org/)

## 🤝 Support

For issues or questions about the chatbot:
1. Check this documentation
2. Review error logs in terminal
3. Verify API key is valid and has credits
4. Check OpenAI service status

---

Built with ❤️ for mental health and wellness education.
