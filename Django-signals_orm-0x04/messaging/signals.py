from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, no edits yet
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Log old content
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.sender  # store who is editing
        )
        instance.edited = True
        instance.edited_by = instance.sender
        
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Clean up messages, notifications, and history when a user is deleted.
    """

    # Delete all messages sent or received by this user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications belonging to this user
    Notification.objects.filter(user=instance).delete()

    # Delete message edit history related to their messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

    print(f"Deleted all related data for user: {instance.username}")


