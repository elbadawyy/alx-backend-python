from django.urls import path
from .views import view_thread

urlpatterns = [
    path("thread/<int:message_id>/", view_thread, name="view_thread"),
]
