from django.contrib import admin
from .models import Restaurant, Category, CustomUser


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant_name', 'budget')
    search_fields = ('restaurant_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, UserAdmin)