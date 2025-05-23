# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class ApprovedUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password) and user.userprofile.is_approved:
                return user
        except UserModel.DoesNotExist:
            return None
        return None
