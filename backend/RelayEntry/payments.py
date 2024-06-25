import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(amount, payment_method_id, billing_info, race_name='', full_name='', team_name=''):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            return_url="http://localhost:8080/confirmation",  # TODO: Update with your actual return URL
            payment_method=payment_method_id,
            confirmation_method='automatic',
            confirm=True,
            metadata={
                'race_name': race_name,
                'registrant_name': full_name,
                'billing_email': billing_info['email'],
                'team_name': team_name,
            },
        )
        return intent
    except stripe.error.CardError as e:
        return {'status': 'card_error', 'message': e.user_message}
    except stripe.error.RateLimitError as e:
        return {'status': 'rate_limit_error', 'message': 'Too many requests made to the API too quickly'}
    except stripe.error.InvalidRequestError as e:
        return {'status': 'invalid_request_error', 'message': e.user_message}
    except stripe.error.AuthenticationError as e:
        return {'status': 'authentication_error', 'message': 'Authentication with Stripe\'s API failed'}
    except stripe.error.APIConnectionError as e:
        return {'status': 'api_connection_error', 'message': 'Network communication with Stripe failed'}
    except stripe.error.StripeError as e:
        return {'status': 'stripe_error', 'message': 'An error occurred with the payment'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
