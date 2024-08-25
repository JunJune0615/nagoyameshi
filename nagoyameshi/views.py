from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin #ログインしたら見れる
from .forms import UserChangeForm
from django.urls import reverse_lazy
from .models import CustomUser

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'nagoyameshi/profile.html'



class UserChangeView(LoginRequiredMixin, UpdateView):
    template_name = 'nagoyameshi/username_edit.html'
    form_class = UserChangeForm
    model = CustomUser
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.request.user.username)
