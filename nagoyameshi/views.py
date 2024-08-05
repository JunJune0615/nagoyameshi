from django.shortcuts import render

from django.views.generic import TemplateView, ListView, CreateView
from .models import Restaurant

#下記form作成のため追加
from .forms import SignUpForm, LoginFrom
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as BaseLoginView,  LogoutView as BaseLogoutView


class TopView(TemplateView):
    template_name = "top.html"

class ProductListView(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"


class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "index.html"

class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "nagoyameshi/signup.html"
    success_url = reverse_lazy("nagoyameshi:index")

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response
    
# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "nagoyameshi/login.html"

# LogoutViewを追加
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("nagoyameshi:index")