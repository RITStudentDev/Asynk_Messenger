from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task
import json
import uuid

from .models import Message
from .tasks import process_pending_messages 

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def send_message_view(request):
    """
    API endpoint to send a message.
    Adds meesage to DB and queues it for sending.
    Expects JSON payload with 'recieverId', 'senderId', and 'content'.
    """

    try:
        data = json.loads(request.body)

        # Ensures required fields are filled
        required_fields = ['recieverId', 'senderId', 'content']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)
            
        # Create new message
        message = Message.objects.create(
            messageId=str(uuid.uuid4()),
            senderId=data['senderId'],
            recieverId=data['recieverId'],
            content=data['content']
        )

        # Adds message to delivery processing queue
        task_id = async_task(process_pending_messages, message.messageId)

        return JsonResponse({
            'success': True,
            'messageId': message.messageId,
            'taskId': task_id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
