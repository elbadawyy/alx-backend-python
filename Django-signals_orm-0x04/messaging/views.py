from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .utils import get_thread


@login_required
def delete_user(request):
    user = request.user
    logout(request)      # log them out first
    user.delete()        # triggers post_delete signal
    return redirect("/") # redirect anywhere you want

@login_required
def view_thread(request, message_id):
    """
    View to return a full threaded conversation for a single message.
    """
    # Optimize database hits
    message_query = (
        Message.objects
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies")
    )

    message = get_object_or_404(message_query, id=message_id)

    # Build recursive thread
    thread = get_thread(message)

    return JsonResponse(thread, safe=False)
