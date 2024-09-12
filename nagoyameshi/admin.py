from django.contrib import admin
from .models import Restaurant, Category, CustomUser, Review


admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Review)
