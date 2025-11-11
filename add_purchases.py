from app import create_app
from models import db, User, Purchase

app = create_app()

with app.app_context():
    # Find all users and show them
    users = User.query.all()
    print(f"\nFound {len(users)} user(s) in database:")
    for u in users:
        print(f"  - {u.email} (ID: {u.id})")
    
    if not users:
        print("No users found! Please register first.")
        exit()
    
    # Use the first user (or you can specify email)
    user = users[0]
    print(f"\nAdding purchases for: {user.email}")
    
    # Create purchases for courses 1, 2, 3, 4
    course_ids = [1, 2, 3, 4]
    
    for course_id in course_ids:
        existing_purchase = Purchase.query.filter_by(
            user_id=user.id,
            module_id=course_id
        ).first()
        
        if not existing_purchase:
            purchase = Purchase(
                user_id=user.id,
                module_id=course_id,
                plan_type='one-time',
                payment_status='completed',
                stripe_payment_id=f'test_purchase_{course_id}'
            )
            db.session.add(purchase)
            print(f"  ✓ Created purchase for course {course_id}")
        else:
            if existing_purchase.payment_status != 'completed':
                existing_purchase.payment_status = 'completed'
                print(f"  ✓ Updated purchase status for course {course_id}")
            else:
                print(f"  - Purchase already exists for course {course_id}")
    
    db.session.commit()
    print("\n✅ All purchases created/updated successfully!")
    print("You can now access all course lessons!")
