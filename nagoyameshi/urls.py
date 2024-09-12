from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.TopView.as_view(), name='top'),
    path('restaurant/<int:restaurant_id>/',views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('account/', include('allauth.urls')), 
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('profile/change/', views.UserChangeView.as_view(), name='profiel_change'),
    path('credit/register/', views.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update/', views.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel/', views.SubscriptionCancelView.as_view(), name='subscription-cancel'),
    path('restaurant/favorite/<int:restaurant_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('restaurant/favorite/list/', views.FavoriteListView.as_view(), name='favorite_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)