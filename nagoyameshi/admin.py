from django.contrib import admin
from .models import Restaurant, Category


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant_name', 'budget')
    search_fields = ('restaurant_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)