from django.contrib.auth.backends import BaseBackend

from django.contrib.auth import get_user_model


from pets_app.models import UserModel

from django.core.exceptions import ValidationError

User = get_user_model()

class SomeBaseBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        model_user = User.objects.get('username')
        model_pass = User.objects.get('passphrase')
        
        if model_user == username and model_pass == password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise ValidationError('User do not exist.')
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None