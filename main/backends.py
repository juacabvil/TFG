from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
import logging

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            logging.warning(f"Password mismatch for user: {user.email}")


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
