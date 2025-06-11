from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect
from django.db.models import Prefetch

@login_required
def message_history_view(request, message_id):
    message = get_object_or_404(Message, id = message_id)
    history = message.message_history.select_related('message').all() # type: ignore
    return render(request, 'messaging/messageHistory.html', {
        'message': message,
        'history': history
    })
    
def delete_user_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'messaging/delete_account.html')

@login_required
def threaded_conversation_view(request, message_id):
    """
    Displays a specific message and all its threaded replies in a recursive format.

    - Fetches the main message and its direct replies using optimized queries.
    - Recursively retrieves nested replies to form a complete threaded conversation.
    - Ensures all user (sender/receiver) details are prefetched to avoid N+1 queries.
    """

    # Get the original message, prefetching replies and user relationships
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'receiver').order_by('timestamp')
            )
        ),
        id=message_id
    )

    # Recursive function to collect all nested replies (threaded messages)
    def fetch_replies(msg):
        replies = Message.objects.filter(parent_message=msg).select_related('sender', 'receiver').order_by('timestamp')
        result = []
        for reply in replies:
            result.append(reply)
            result.extend(fetch_replies(reply))  # Recursively get deeper replies
        return result

    all_replies = fetch_replies(message)

    # Render the thread with the original message and all nested replies
    return render(request, 'messaging/thread.html', {
        'message': message,
        'all_replies': all_replies
    })


@login_required
def reply_to_message(request, message_id):
    """
    Handles reply form submission to a specific message.

    - Expects POST request with 'content' and 'receiver'.
    - Creates a new Message instance linked to the parent message.
    """
    parent = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver')
        receiver = get_object_or_404(User, id=receiver_id)

        # Create reply message
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent
        )

        return redirect('threaded_conversation_view', message_id=message_id)

    return render(request, 'messaging/reply.html', {'parent': parent})
