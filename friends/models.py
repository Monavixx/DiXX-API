from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class FriendRequest (models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_from_me')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_to_me')
    request_datetime = models.DateTimeField(auto_now_add=True)