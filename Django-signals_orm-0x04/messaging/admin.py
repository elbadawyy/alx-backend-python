from django.contrib import admin

# Register your models here.
from .models import Message, Notification

# Register your models
admin.site.register(Message)
admin.site.register(Notification)
