from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import EmailValidator



class DiXXUserManager(UserManager):
    pass

class DiXXUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices={'m':'man', 'w': 'woman'}, blank=True, null=True)
    objects = DiXXUserManager()
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)