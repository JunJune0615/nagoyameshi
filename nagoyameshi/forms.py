from django.forms import ModelForm
from .models import CustomUser

class UserChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username'
        ]
