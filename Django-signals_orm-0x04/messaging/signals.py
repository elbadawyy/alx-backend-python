from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification

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

