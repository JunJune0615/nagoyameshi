from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.TopView.as_view(), name='top'),
    path('restaurant/<int:restaurant_id>/',views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('account/', include('allauth.urls')), 
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('profile/change/', views.UserChangeView.as_view(), name='profiel-change'),
    path('profiele/favorite/list/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('profiele/booking/list/', views.BookingListView.as_view(), name='booking-list'),
    path('credit/register/', views.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update/', views.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel/', views.SubscriptionCancelView.as_view(), name='subscription-cancel'),
    path('restaurant/favorite/<int:restaurant_id>/', views.toggle_favorite, name='toggle-favorite'),
    path('restaurant/review_create/<int:restaurant_id>/', views.ReviewCreateView.as_view(), name='review-create'),
    path('restaurant/review_update/<int:pk>/', views.ReviewUpdateView.as_view(), name='review-update'),
    path('restaurant/review_delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review-delete'),
    path('restaurant/calendar/<int:restaurant_id>/', views.BookingCalendar.as_view(), name='calendar'),
    path('restaurant/calendar/<int:restaurant_id>/<int:year>/<int:month>/<int:day>/', views.BookingCalendar.as_view(), name='calendar'),
    path('restaurant/booking/<int:restaurant_id>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Booking.as_view(), name='booking'),
    path('restaurant/booking_update/<int:pk>/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('restaurant/booking_delete/<int:pk>/', views.BookingDeleteView.as_view(), name='booking-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)