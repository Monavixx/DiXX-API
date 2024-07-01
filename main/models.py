from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError


class DiXXUserManager(UserManager):
    pass

class DiXXUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices={'m':'man', 'w': 'woman'}, blank=True, null=True)
    objects = DiXXUserManager()

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        #BAD_SYMBOLS = ' \t\n'
        #print(self.username)
        #for bs in BAD_SYMBOLS:
        #    if bs in self.username:
        #        raise ValidationError('Username must not contains \'' + bs + '\' symbol.')
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)