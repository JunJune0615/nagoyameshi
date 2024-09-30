from django.contrib import admin
from .models import Restaurant, Category, CustomUser, Review, FavoriteRestaurant, RestaurantBooking

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('email',)

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(FavoriteRestaurant)
admin.site.register(RestaurantBooking)