from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError


class DiXXUserManager(UserManager):
    pass

class DiXXUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices={'m':'man', 'w': 'woman'}, blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    objects = DiXXUserManager()

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username