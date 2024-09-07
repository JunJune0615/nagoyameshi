import requests
import stripe

from myproject import settings

from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin #ログインしたら見れる
from .forms import UserChangeForm
from django.urls import reverse_lazy
from .models import CustomUser, Restaurant
from django.shortcuts import render, redirect


class TopView(ListView):
    model = Restaurant
    paginate_by = 10
    template_name = 'nagoyameshi/top.html'


class RestaurantDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')

    model = Restaurant

    template_name = 'nagoyameshi/restaulant_detail.html'
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return render(request,"nagoyameshi/restaulant_detail.html",{"restaurant": restaurant})
    

class ProfileView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')

    template_name = 'nagoyameshi/profile.html'


class UserChangeView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('top')

    raise_exception = False
    login_url = reverse_lazy('top')
    
    template_name = 'nagoyameshi/username_edit.html'
    form_class = UserChangeForm
    model = CustomUser
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.request.user.username)


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreditRegisterView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')

    raise_exception = False
    login_url = reverse_lazy('top')

    def get(self, request):
        ctx = {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'nagoyameshi/register.html', ctx)

    def post(self, request):
        email = self.request.user.email
        customer = stripe.Customer.create(
            name=email,
            email=email,
        )

        card = stripe.Customer.create_source(
            customer.id,
            source=request.POST['stripeToken'],
        )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': settings.STRIPE_PRICE_ID}],
        )

        custom_user = CustomUser.objects.get(email=email)
        custom_user.stripe_customer_id = customer.id
        custom_user.stripe_card_id = card.id
        custom_user.stripe_subscription_id = subscription.id
        custom_user.vip_member = True
        custom_user.save()

        return redirect('top')


class SubscriptionCancelView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')

    def get(self, request):
        return render(request, 'nagoyameshi/subscription_cancel.html')

    def post(self, request):
        custom_user = CustomUser.objects.get(email=request.user.email)
        stripe.Subscription.delete(custom_user.stripe_subscription_id)
        stripe.Customer.delete(custom_user.stripe_customer_id)

        custom_user.stripe_customer_id = None
        custom_user.stripe_card_id = None
        custom_user.stripe_subscription_id = None
        custom_user.vip_member = False
        custom_user.save()

        return redirect('top')


class CreditUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')

    def get(self, request):
        email = self.request.user.email
        custom_user = CustomUser.objects.get(email=email)
        url = f'https://api.stripe.com/v1/customers/{custom_user.stripe_customer_id}/cards/{custom_user.stripe_card_id}'
        response = requests.get(url, auth=(settings.STRIPE_SECRET_KEY, ''))

        stripe_customer_json = response.json()

        ctx = {
            'card_brand': stripe_customer_json['brand'],
            'card_last4': stripe_customer_json['last4'],
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'nagoyameshi/update.html', ctx)

    def post(self, request):
        email = self.request.user.email
        custom_user = CustomUser.objects.get(email=email)

        card = stripe.Customer.create_source(
            custom_user.stripe_customer_id,
            source=request.POST['stripeToken'],
        )

        stripe.Customer.delete_source(
            custom_user.stripe_customer_id,
            custom_user.stripe_card_id,
        )

        custom_user.stripe_card_id = card.id
        custom_user.save()

        return redirect('top')
