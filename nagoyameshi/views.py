import requests
import stripe
import datetime
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from myproject import settings
from django.views.generic import TemplateView, View, ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin 
from .forms import UserChangeForm, RestaurantSearchForm, ReviewForm, ReviewCreateForm, BookingForm
from django.urls import reverse_lazy, reverse
from .models import CustomUser, Restaurant, Review, FavoriteRestaurant, RestaurantBooking
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
# https://nissin-geppox.hatenablog.com/entry/2022/09/10/221409

class TopView(ListView):
    model = Restaurant
    paginate_by = 10
    template_name = 'nagoyameshi/top.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = RestaurantSearchForm(self.request.GET or None)
        if form.is_valid():
            # カテゴリ名で絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            #　レストラン名で絞り込み
            restaurant_name = form.cleaned_data.get('restaurant_name')
            if restaurant_name:
                queryset = queryset.filter(restaurant_name__icontains=restaurant_name) 
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # search formを渡す
        context['search_form'] = self.form
        return context


class RestaurantDetailView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated 

    def handle_no_permission(self):
        return redirect('account_login')
    
    raise_exception = False
    login_url = reverse_lazy('account_login')
    model = Restaurant
    template_name = 'nagoyameshi/restaulant_detail.html'

    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        favorite = FavoriteRestaurant.objects.filter(restaurant_id=restaurant.id, user_id=request.user.id).first
        reviews = Review.objects.filter(restaurant_id=restaurant.id)
        is_review = reviews.filter(user_id=request.user.id).exists
        return render(request, "nagoyameshi/restaulant_detail.html", {"restaurant": restaurant, "favorite": favorite, "reviews": reviews, "is_review": is_review})


def toggle_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.user.vip_member:
        favorite_restaurant, created = FavoriteRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)
        if not created:
            favorite_restaurant.delete()
        return redirect('restaurant-detail', restaurant_id=restaurant.id)
    else:
        return redirect('credit-register')


class FavoriteListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')

    raise_exception = False
    login_url = reverse_lazy('top')
    model = Restaurant
    paginate_by = 10
    template_name = 'nagoyameshi/favorite_list.html'

    def get_queryset(self):
        favorites = FavoriteRestaurant.objects.filter(user_id=self.request.user.id)
        restaurant_ids = [favorite.restaurant_id for favorite in favorites]
        queryset = super().get_queryset()
        return queryset.filter(id__in=restaurant_ids)


class ReviewCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')
    model = Review
    form_class = ReviewForm
    template_name = 'nagoyameshi/review_create.html'

    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return render(request, "nagoyameshi/review_create.html", {"restaurant": restaurant})

    def get_success_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': int(self.kwargs['restaurant_id'])})
    
    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "レビューを書いてください")
        return redirect('top')


class ReviewUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    template_name = 'nagoyameshi/review_update.html'
    form_class = ReviewCreateForm
    model = Review

    def get_success_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': int(self.object.restaurant.pk)})
    
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user_id=self.request.user.id)
        restaurant = get_object_or_404(Restaurant, restaurant_name=review.restaurant)
        return render(request, "nagoyameshi/review_update.html", {"review": review, "restaurant": restaurant})

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        return super().form_valid(form)


class ReviewDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    model = Review
    template_name = 'nagoyameshi/review_delete.html'

    def get_success_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': int(self.object.restaurant.pk)})

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user_id=self.request.user.id)
        restaurant = get_object_or_404(Restaurant, restaurant_name=review.restaurant)
        return render(request, "nagoyameshi/review_delete.html", {"review": review, "restaurant": restaurant})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


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
        return redirect('profile')


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
        return redirect('profile')


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
        return redirect('profile')


class BookingCalendar(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')
    template_name = 'nagoyameshi/booking_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        today = datetime.date.today()
        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today
         # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]
        # 開店時間と閉店時間の入手
        open_time = restaurant.open_time
        close_time = restaurant.close_time
        # 開店時間と閉店時間の時間を入手
        open_hour = int(open_time.hour)
        end_hour = int(close_time.hour)
        # 開店時間より閉店時間のほうが大きいときは開店時間をstartに閉店時間をfinishに、小さいときはstartに0とfinishに24を代入
        if open_hour >= end_hour:
            start_hour_false = end_hour
            finish_hour_false = open_hour
        else:
            start_hour_false = 0
            finish_hour_false = 24
        # 0時から24時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(0, 24):
            calendar[hour] = {}
            for day in days:
                if (open_hour > hour and hour >= start_hour_false) or (end_hour <= hour and hour < finish_hour_false):
                    calendar[hour][day] = False
                else:
                    calendar[hour][day] = True
        #予約しているものをFalseとする
        for schedule in RestaurantBooking.objects.filter(restaurant=restaurant):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = int(local_dt.hour)
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date] = False
        #contextのまとめ
        context['restaurant'] = restaurant
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        return context


class Booking(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    raise_exception = False
    login_url = reverse_lazy('top')
    template_name = 'nagoyameshi/booking.html'
    model = RestaurantBooking
    form_class = BookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        return context

    def form_valid(self, form):
        #レストランと時間を入手
        restaurant =  get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        today = datetime.date.today()
        open_time = restaurant.open_time
        close_time = restaurant.close_time
        open_hour = int(open_time.hour)
        end_hour = int(close_time.hour)
        # 開店時間より閉店時間のほうが大きいときは開店時間をstartに閉店時間をfinishに、小さいときはstartに0とfinishに24を代入
        if open_hour >= end_hour:
            start_hour_false = end_hour
            finish_hour_false = open_hour
        else:
            start_hour_false = 0
            finish_hour_false = 24
        #不正の時間や入れ違いの予約があった際にキャンセルする当てはまらないときはよやくをする
        if RestaurantBooking.objects.filter(restaurant=restaurant, start=start).exists():
            messages.error(self.request, '入れ違いで予約がありました。お手数をおかけしますが別の日時を選択してください。')
        elif start.date() <= today:
            messages.error(self.request, '予約日時は翌日以降にしてください。')
        elif (open_hour > hour and hour >= start_hour_false) or (end_hour <= hour and hour < finish_hour_false):
            messages.error(self.request, '予約時間は営業時間内にしてください。')
        else:
            booking = form.save(commit=False)
            booking.user = self.request.user
            booking.restaurant = restaurant
            booking.start = start
            booking.end = end
            booking.save()
        return redirect('booking-list')


class BookingListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')

    raise_exception = False
    login_url = reverse_lazy('top')
    model = Restaurant
    paginate_by = 10
    template_name = 'nagoyameshi/booking_list.html'

    def get_queryset(self):
        queryset = RestaurantBooking.objects.filter(user_id=self.request.user.id).order_by('start')
        return queryset


class BookingUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    template_name = 'nagoyameshi/booking_update.html'
    form_class = BookingForm
    model = RestaurantBooking
    success_url = reverse_lazy('booking-list')

    def get(self, request, pk):
        booking = get_object_or_404(RestaurantBooking, pk=pk, user_id=self.request.user.id)
        today = datetime.date.today()
        form = BookingForm()
        if today >= booking.start.date():
            messages.error(self.request, '当日より以前のものは人数変更できません。お店へ連絡してください')
            return redirect('booking-list')
        return render(request, "nagoyameshi/booking_update.html", {"booking": booking, 'form': form})

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "予約人数は10人までです")
        return redirect('booking-list')


class BookingDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.vip_member

    def handle_no_permission(self):
        return redirect('top')
    
    model = RestaurantBooking
    template_name = 'nagoyameshi/booking_delete.html'
    success_url = reverse_lazy('booking-list')

    def get(self, request, pk):
        booking = get_object_or_404(RestaurantBooking, pk=pk, user_id=self.request.user.id)
        today = datetime.date.today()
        if today >= booking.start.date():
            messages.error(self.request, '当日より以前のものはキャンセルできません。お店へ連絡してください')
            return redirect('booking-list')
        return render(request, "nagoyameshi/booking_delete.html", {"booking": booking})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
