from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.stk_push_service import send_stk_push


@csrf_exempt
def stk_push(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = send_stk_push(request)
        return JsonResponse(data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
