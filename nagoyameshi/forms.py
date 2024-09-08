from django.forms import ModelForm
from .models import CustomUser, Category
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

