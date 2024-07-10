import stripe
from django.conf import settings
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY

# Set up logging
logger = logging.getLogger(__name__)

def retrieve_payment_intent(payment_intent_id, race):
    try:
        race_id = race.id
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        amount = intent.amount
        amount_received = intent.amount_received
        status = intent.status

        logger.info(f"Race ID: {race_id}, PaymentIntent ID: {payment_intent_id}, Amount: {amount}, Amount Received: {amount_received}, Status: {status}")

        return intent, None

    except Exception as e:
        logger.error(f"Error retrieving PaymentIntent for Race ID {race_id}, PaymentIntent ID {payment_intent_id}: {e}")
        return None, str(e)
