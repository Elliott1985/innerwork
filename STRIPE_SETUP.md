# Stripe Payment & Email Integration

## Overview
InnerWork now includes Stripe payment processing and email confirmation functionality for course purchases.

## What's New

### 1. **Stripe Payment Integration**
   - Users can purchase courses via Stripe Checkout (test mode by default)
   - Secure payment processing with automatic enrollment creation
   - Payment verification via Stripe session IDs

### 2. **Email Notifications**
   - Purchase confirmation emails sent automatically
   - Graceful fallback to console logging if SMTP not configured
   - Uses Flask-Mail for email delivery

### 3. **Dashboard System**
   - Track course enrollment and progress (0-100%)
   - Mark courses as complete
   - Quick progress update buttons for demo purposes
   - Schedule 1:1 sessions via integrated booking page

### 4. **Booking Integration**
   - Calendly embed for scheduling 1:1 sessions
   - Beautiful UI with session details
   - Direct link from dashboard

## Environment Variables

Add these to your `.env` file:

```env
# Stripe Configuration
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx

# Mail Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=InnerWork <no-reply@innerwork.demo>
```

### Getting Stripe Test Keys
1. Sign up at https://dashboard.stripe.com/register
2. Go to Developers → API keys
3. Copy your **Publishable key** (starts with `pk_test_`)
4. Copy your **Secret key** (starts with `sk_test_`)
5. Replace the placeholder values in `.env`

### Test Card Numbers (Stripe Test Mode)
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Use any future expiry date and any 3-digit CVC

## New Routes

### Dashboard
- `GET /dashboard` - User's course dashboard with progress tracking
- `POST /dashboard/progress/<module_id>/<percent>` - Update progress

### Stripe Payments
- `POST /stripe/purchase/<module_id>` - Create Stripe checkout session
- `GET /stripe/purchase/success/<module_id>` - Handle successful payment

### Booking
- `GET /book` - Calendly integration for 1:1 sessions

## Database Changes

New `enrollments` table tracks user progress:
```sql
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    progress INTEGER DEFAULT 0,     -- 0-100 percentage
    status VARCHAR(20) DEFAULT 'in_progress',  -- 'in_progress' or 'complete'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

New columns in `modules` table:
- `price_cents` (INTEGER) - Price in cents for Stripe
- `duration_label` (VARCHAR) - Display label like "4 Modules"

## Files Created/Modified

### New Files
- `routes/dashboard.py` - Dashboard blueprint
- `routes/stripe_payments.py` - Stripe integration
- `routes/booking.py` - Calendly booking page
- `templates/dashboard/index.html` - Dashboard UI
- `templates/book.html` - Booking page
- `migrate_db.py` - Database migration script

### Modified Files
- `app.py` - Added Flask-Mail and Stripe configuration
- `models.py` - Added Enrollment model and new Module fields
- `routes/courses.py` - Added price_cents to course data
- `templates/courses/detail.html` - Added Stripe checkout button
- `.env` - Added Stripe and mail configuration

## Usage Flow

1. **User browses courses** at `/courses/`
2. **Clicks course** to view details at `/courses/<id>`
3. **Clicks "Enroll Now"** button
4. **Redirected to Stripe Checkout** (test mode)
5. **Enters test card**: 4242 4242 4242 4242
6. **Completes payment** → redirected to success page
7. **Enrollment created** in database
8. **Email sent** (or logged to console if no SMTP)
9. **Redirected to dashboard** showing enrolled course
10. **Can track progress** and mark lessons complete

## Email Fallback

If SMTP is not configured (or credentials are invalid), emails will be printed to the console instead of failing silently. This ensures the demo works without requiring email setup.

Example console output:
```
--- EMAIL (console fallback) ---
To: user@example.com
Subject: InnerWork: Purchase Confirmed – I Am Not My Trauma
<HTML email content>
--- END EMAIL ---
```

## Testing Checklist

- [ ] Browse courses at `/courses/`
- [ ] Click a course to view details
- [ ] Click "Enroll Now" (while logged in)
- [ ] Complete Stripe checkout with test card
- [ ] Verify enrollment appears in dashboard
- [ ] Check console for email confirmation (if SMTP not set up)
- [ ] Update progress using +10% button
- [ ] Mark course as complete
- [ ] Access booking page via dashboard
- [ ] View Virtual Elliott on lesson pages

## Production Considerations

1. **Replace test Stripe keys** with live keys in `.env`
2. **Configure real SMTP** credentials (Gmail, SendGrid, etc.)
3. **Update Calendly URL** in `templates/book.html` with real link
4. **Implement Stripe webhooks** for payment verification
5. **Add rate limiting** on payment endpoints
6. **Enable HTTPS** for secure payment processing
7. **Consider PostgreSQL** instead of SQLite
8. **Add proper error handling** and user notifications
9. **Implement refund handling** if needed
10. **Add purchase receipts** as PDFs or detailed email formatting

## Support

For Stripe issues: https://stripe.com/docs
For Flask-Mail issues: https://pythonhosted.org/Flask-Mail/
