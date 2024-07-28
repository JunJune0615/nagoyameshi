from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Restaurant

class TopView(TemplateView):
    template_name = "top.html"

class ProductListView(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"