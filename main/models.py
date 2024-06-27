from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class DiXXUserManager(UserManager):
    pass

class DiXXUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices={'m':'man', 'w': 'woman'}, blank=True, null=True)
    objects = DiXXUserManager()