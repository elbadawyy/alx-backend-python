# messaging/utils.py

def get_thread(message):
    """
    Recursively fetch a message and all nested replies.
    Returns a nested dictionary structure suitable for rendering in UI.
    """

    thread = {
        "id": message.id,
        "content": message.content,
        "sender": message.sender.username,
        "timestamp": message.timestamp,
        "replies": []
    }

    # Load replies in chronological order
    for reply in message.replies.all().order_by("timestamp"):
        thread["replies"].append(get_thread(reply))

    return thread
