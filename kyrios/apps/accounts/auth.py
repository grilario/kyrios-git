import re
import base64

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate

checkEmail = re.compile(
    r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            return None

        if re.fullmatch(checkEmail, username):
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None
            else:
                if user.check_password(password):
                    return user
            return None

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None


def base_auth(authorization_header):
    authmeth, auth = authorization_header.split(' ', 1)
    if authmeth.lower() == 'basic':
        auth = base64.b64decode(auth.strip()).decode('utf8')
        username, password = auth.split(':', 1)
        user = authenticate(username=username, password=password)
        return user
    else:
        return None