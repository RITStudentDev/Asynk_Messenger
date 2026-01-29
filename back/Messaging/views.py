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
def send_message(request):
    """
    API endpoint to send a message.
    Adds message to DB and queues it for sending.
    Expects JSON payload with 'receiverId', 'senderId', and 'content'.
    """

    try:
        data = json.loads(request.body)

        # Ensures required fields are filled
        required_fields = ['receiverId', 'senderId', 'content']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)
            
        # Create new message
        message = Message.objects.create(
            messageId=str(uuid.uuid4()),
            senderId=data['senderId'],
            receiverId=data['receiverId'],
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

@require_http_methods(["GET"])
def get_messages(request, user_id):
    """
    Gets messages which are set to be sent to user with user_id.
    """
    messages = Message.objects.filter(receiverId=user_id).values(
        'messageId', 'senderId', 'content', 'timestamp', 'status'
    )

    return JsonResponse({'messages': list(messages)}, status=200)