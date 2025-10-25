import stripe
from config import STRIPE_SECRET_KEY, PAID_PLAN_PRICE_ID

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(email):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=email,
        line_items=[{
            'price': PAID_PLAN_PRICE_ID,
            'quantity': 1,
        }],
        mode='subscription',
        success_url='http://localhost:8501/?success=true&email={CHECKOUT_EMAIL}',
        cancel_url='http://localhost:8501/?canceled=true',
    )
    return session.url