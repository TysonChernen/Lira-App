from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models

# Define trial duration (e.g., 7 days)
TRIAL_DAYS = 7

def start_free_trial(user_id: int, plan: str, db: Session):
    """Start a free trial for the given user"""
    existing_sub = db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()

    if existing_sub:
        return {"error": "User already has an active subscription or trial"}

    trial_end_date = datetime.utcnow() + timedelta(days=TRIAL_DAYS)

    new_subscription = models.Subscription(
        user_id=user_id,
        plan=plan,
        is_trial=True,
        start_date=datetime.utcnow(),
        end_date=trial_end_date
    )
    
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    
    return {"message": f"Free trial for {plan} started. Expires on {trial_end_date}"}

def upgrade_to_paid(user_id: int, plan: str, db: Session):
    """Upgrade user to a full paid subscription"""
    sub = db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()

    if not sub:
        return {"error": "User does not have an active trial"}

    sub.is_trial = False
    sub.start_date = datetime.utcnow()
    sub.end_date = None  # No end date for full subscriptions

    db.commit()
    
    return {"message": f"User upgraded to paid {plan} subscription"}

