# Vercel Deployment Guide for InnerWork

## Overview

This guide covers deploying InnerWork to Vercel with mobile optimizations. The deployment requires migrating from SQLite to PostgreSQL and configuring external session storage.

## ⚠️ Important Prerequisites

Vercel's serverless environment has limitations:
- **No SQLite support** (ephemeral filesystem) → Must use PostgreSQL
- **No local file sessions** → Must use Redis or database sessions
- **Serverless functions** → Cold starts possible

## Mobile Optimizations Implemented

✅ **Responsive CSS**
- Touch-friendly tap targets (44px minimum)
- Mobile-first breakpoints (768px, 576px)
- iOS zoom prevention (16px font inputs)
- Landscape orientation support
- Touch device hover state handling

✅ **PWA Meta Tags**
- Mobile viewport settings
- Theme color (#c59fc9 lavender)
- Apple mobile web app support
- Progressive web app capabilities

## Step 1: Database Setup (PostgreSQL)

### Option A: Vercel Postgres (Recommended)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Link your project:
```bash
vercel link
```

3. Create Postgres database:
```bash
vercel postgres create innerwork-db
```

4. Link database to project:
```bash
vercel postgres link innerwork-db
```

This automatically sets `POSTGRES_URL` environment variable.

### Option B: External PostgreSQL (Heroku, Railway, Neon, etc.)

1. Create a PostgreSQL database on your preferred provider
2. Note the connection URL (format: `postgresql://user:password@host:port/database`)
3. Add as environment variable in Vercel dashboard

## Step 2: Session Storage (Redis)

### Option A: Vercel KV (Redis-compatible)

1. Create KV storage:
```bash
vercel kv create innerwork-sessions
```

2. Link to project:
```bash
vercel kv link innerwork-sessions
```

### Option B: External Redis (Upstash, Redis Cloud)

1. Create Redis instance
2. Get connection URL: `redis://default:password@host:port`
3. Add as `REDIS_URL` environment variable

### Option C: Database Sessions (Alternative)

If you prefer not to use Redis, modify `app.py` to use database sessions:

```python
# Replace filesystem sessions with database sessions
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
```

## Step 3: Configure Environment Variables

In Vercel dashboard (Settings → Environment Variables), add:

**Required:**
- `FLASK_SECRET_KEY` - Random secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL` - PostgreSQL connection string (auto-set if using Vercel Postgres)
- `OPENAI_API_KEY` - Your OpenAI API key for chatbot

**Stripe:**
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_PUBLIC_KEY` - Stripe publishable key

**Mail (Optional):**
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`

**Session Storage:**
- `REDIS_URL` - Redis connection URL (if using Redis sessions)

**Environment:**
- `FLASK_ENV=production`

## Step 4: Update App Configuration for Vercel

Modify `app.py` to support PostgreSQL and Redis:

```python
import os
from flask import Flask
from flask_session import Session
import redis

def create_app():
    app = Flask(__name__)
    
    # Use DATABASE_URL from environment (Vercel Postgres)
    database_url = os.getenv('DATABASE_URL', 'sqlite:///db/innerwork.db')
    
    # Vercel Postgres uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    # Configure Redis sessions (if REDIS_URL available)
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_REDIS'] = redis.from_url(redis_url)
    else:
        # Fallback to database sessions for Vercel
        app.config['SESSION_TYPE'] = 'sqlalchemy'
        app.config['SESSION_SQLALCHEMY'] = db
    
    # Rest of configuration...
```

## Step 5: Deploy to Vercel

### Using Vercel CLI (Recommended)

1. Install dependencies locally first:
```bash
pip install -r requirements.txt
```

2. Deploy:
```bash
vercel --prod
```

### Using GitHub Integration

1. Push code to GitHub
2. Import repository in Vercel dashboard
3. Configure environment variables
4. Deploy automatically on push

## Step 6: Database Migration

After first deployment, initialize database tables:

1. Use Vercel CLI to run commands:
```bash
vercel env pull .env.production
```

2. Create a migration script `migrate.py`:
```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
```

3. Run locally against production database:
```bash
python migrate.py
```

Or use Vercel's serverless function to create tables on first request.

## Step 7: Testing

Test the mobile-optimized deployment:

1. **Desktop browser**: Open DevTools → Toggle device toolbar
2. **Real device**: Visit your Vercel URL on mobile
3. **Lighthouse**: Run mobile performance audit

### Test checklist:
- ✅ Responsive layout on various screen sizes
- ✅ Touch targets are 44px+ (accessible)
- ✅ Forms don't trigger zoom on iOS
- ✅ Navigation collapses properly on mobile
- ✅ Chat interface scrollable on mobile
- ✅ Videos responsive
- ✅ Login/registration works
- ✅ Chatbot conversation persists
- ✅ Stripe checkout functional

## Troubleshooting

### Cold Start Issues
Vercel serverless functions may have cold starts. Consider:
- Using Vercel Pro for reduced cold starts
- Implementing loading states in UI
- Using static generation where possible

### Session Issues
If sessions aren't persisting:
- Verify `REDIS_URL` is set correctly
- Check Redis connection in logs
- Ensure `SESSION_TYPE` is not 'filesystem'

### Database Connection Errors
- Verify `DATABASE_URL` format is `postgresql://` not `postgres://`
- Check connection limits on your database provider
- Use connection pooling if needed

### Static Files Not Loading
- Ensure `vercel.json` routes are correct
- Check `static/` directory structure
- Verify URLs use `url_for('static', filename='...')`

## Performance Optimization

### Recommended Vercel Settings:
- **Function Region**: Choose closest to your users
- **Edge Functions**: Consider for static pages
- **Caching**: Enable for static assets

### Mobile Performance:
- Images should be optimized (WebP, lazy loading)
- Consider PWA service worker for offline support
- Minimize JavaScript bundle size

## Cost Considerations

**Vercel Free Tier:**
- 100GB bandwidth/month
- Serverless function executions limited
- Good for personal/prototype projects

**Vercel Pro ($20/month):**
- 1TB bandwidth
- Better performance
- Recommended for production

**External Services:**
- PostgreSQL: Free tiers available (Neon, Supabase)
- Redis: Free tiers available (Upstash, Redis Cloud)
- Consider costs scaling with users

## Alternative: Traditional Hosting

If Vercel's serverless model doesn't fit:
- **Railway**: Full stack PostgreSQL + Redis included
- **Render**: Free PostgreSQL + background workers
- **Heroku**: Traditional dyno-based hosting
- **DigitalOcean App Platform**: Container-based deployment

These alternatives support SQLite and file sessions out of the box.

## Support

For issues:
1. Check Vercel deployment logs: `vercel logs`
2. Review function logs in Vercel dashboard
3. Test locally with production environment variables
4. Consult Vercel documentation: https://vercel.com/docs

## Next Steps

After successful deployment:
- [ ] Set up custom domain
- [ ] Configure SSL (automatic with Vercel)
- [ ] Set up monitoring/analytics
- [ ] Implement error tracking (Sentry)
- [ ] Add PWA service worker for offline support
- [ ] Configure CDN caching rules
- [ ] Set up CI/CD for automated testing
