from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import CustomUser, Category, Review
from django import forms

class UserChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username'
        ]


class RestaurantSearchForm(forms.Form):
    # カテゴリーフィルター
    category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=Category.objects.order_by('category_name'),
        widget=forms.Select(attrs={'class': 'form'})
    )

    # レストラン名検索
    restaurant_name = forms.CharField(
        label='レストラン名での絞り込み',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form',
                                      'autocomplete': 'off',
                                      'placeholder': '店舗名',
                                      })
    )


class ReviewForm(forms.ModelForm):   
    class Meta:
        model = Review
        fields = ['review', 'restaurant']


class ReviewCreateForm(forms.ModelForm):   
    class Meta:
        model = Review
        fields = ['review', ]

        