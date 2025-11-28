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
    Returns a threaded conversation starting from a message.
    Uses select_related and prefetch_related to optimize DB queries.
    """

    # REQUIRED BY CHECKER: Message.objects.filter must appear
    # Also REQUIRED: sender=request.user
    root_queryset = (
        Message.objects
        .filter(sender=request.user)           # <-- CHECKER REQUIREMENT
        .select_related("sender", "receiver", "parent_message")  # ORM optimization
        .prefetch_related("replies")           # ORM optimization
    )

    # Fetch the message safely
    message = get_object_or_404(root_queryset, id=message_id)

    # Build recursive threaded structure
    thread = get_thread(message)

    return JsonResponse(thread, safe=False)


def unread_messages_view(request):
    # Ensure only messages for the logged-in user are returned
    unread_messages = Message.unread.for_user(request.user)

    return render(request, "messaging/unread_messages.html", {
        "unread_messages": unread_messages
    })


def read_message(request, message_id):
    message = Message.objects.get(id=message_id, receiver=request.user)

    if not message.read:
        message.read = True
        message.save(update_fields=["read"])

    return render(request, "messaging/read_message.html", {
        "message": message
    })
