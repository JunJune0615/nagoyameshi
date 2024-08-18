from django.urls import path, include

from . import views

urlpatterns = [
    path('account/', include('allauth.urls')), 
    path('profile/',views.ProfileView.as_view(), name='profile')
]