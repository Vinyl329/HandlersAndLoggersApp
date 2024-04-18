import django_filters
from django import forms
from django_filters import FilterSet, DateFilter
from .models import Post

class NewsFilter(FilterSet):
    post_time = DateFilter(field_name='date', widget=forms.DateInput(attrs={'type': 'date'}),
                           lookup_expr='date__lt')
    class Meta:
        model = Post
        fields = {
            'statement': ['icontains'],
            'category': ['exact'],
        }