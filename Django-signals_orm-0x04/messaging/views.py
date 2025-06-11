from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory
from django.shortcuts import redirect

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