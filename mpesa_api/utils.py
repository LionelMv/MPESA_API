import requests
from decouple import config
from datetime import datetime
from django.core.cache import cache
import base64
import logging

logger = logging.getLogger('mpesa')


def generate_access_token():
    """
    Get or create an M-PESA access token.
    Reuses cached token if still valid.
    """
    token = cache.get('mpesa_access_token')
    if token:
        logger.info("Using cached M-PESA access token")
        return token

    # If not cached or expired → fetch new one
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_SECRET')
    url = f"{config('MPESA_BASE_URL')}/oauth/v1/generate?grant_type=client_credentials"

    logger.info("Requesting new M-PESA access token...")
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    response.raise_for_status()
    data = response.json()

    token = data.get('access_token')
    expires_in = int(data.get('expires_in', 3600))  # (1 hour)

    # Cache it (slightly less than 1 hour to be safe)
    cache.set('mpesa_access_token', token, timeout=expires_in - 60)

    logger.info(f"New token fetched successfully, expires in {expires_in}s")

    return token


def generate_password():
    """Generates base64-encoded password for STK push."""
    shortcode = config('MPESA_SHORTCODE')
    passkey = config('MPESA_PASSKEY')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    encoded = base64.b64encode(data_to_encode.encode()).decode()

    logger.info(f"Generated password for STK push.")

    return encoded, timestamp
