from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Card(models.Model):
    first = models.CharField(max_length=200)
    second = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_datetime = models.DateTimeField(auto_now = True)
    