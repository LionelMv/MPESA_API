import requests
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_access_token(request):
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_SECRET')
    access_token_url = config('MPESA_ACCESS_TOKEN_URL')
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(
            access_token_url,
            headers=headers,
            auth=(consumer_key, consumer_secret)
            )
        response.raise_for_status()
        data = response.json()
        return JsonResponse({'access_token': data['access_token']})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
