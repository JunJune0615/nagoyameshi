from django.contrib import admin
from .models import Restaurant, Category, CustomUser, Review, FavoriteRestaurant, RestaurantBooking

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('email', 'username',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant_name', 'create_date')
    search_fields = ('restaurant_name',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(FavoriteRestaurant)
admin.site.register(RestaurantBooking)