from django.apps import AppConfig
from django.contrib.auth import get_user_model


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username='AnonymousUser').exists():
            User.objects.create_user(
                username='AnonymousUser',
                email='AnonymousUser@example.com',
                password='password'
            )
            print("AnonymousUser user created.")
        else:
            print("AnonymousUser user already exists.")

