from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Set(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(auto_now_add = True)
    users = models.ManyToManyField(User, related_name='sets')
    is_private = models.BooleanField(default=False)
    @property
    def numberOfCards(self):
        return len(self.card_set.all())

class Card(models.Model):
    first = models.CharField(max_length=200)
    second = models.CharField(max_length=200)
    create_datetime = models.DateTimeField(auto_now = True)
    cardset = models.ForeignKey(Set, on_delete=models.CASCADE)
