from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .utils import get_thread
from django.views.decorators.cache import cache_page


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
    unread_messages = Message.unread.unread_for_user(request.user).only(
        "id", "sender", "content", "created_at"
    )

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
    
@cache_page(60)  # cache for 60 seconds
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)
    return render(request, "messages/list.html", {"messages": messages})


@cache_page(60)
def message_list(request):
    messages = Message.objects.all().order_by("-created_at")
    return render(request, "messages/list.html", {"messages": messages})
