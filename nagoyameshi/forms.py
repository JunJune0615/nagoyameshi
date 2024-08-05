from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
        )

# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = CustomUser