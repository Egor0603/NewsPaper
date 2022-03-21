from django.forms import SelectDateWidget
from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter, CharFilter
from .models import Post, Category
from datetime import datetime

cur_year = datetime.now().year

CY = [year for year in range(cur_year - 10, cur_year + 10)]


class PostFilter(FilterSet):
    cats = ModelMultipleChoiceFilter(queryset=Category.objects.all())
    created_after = DateFilter(label='Created after', lookup_expr='gte', widget=SelectDateWidget(years=CY))
    created_before = DateFilter(label='Created before', lookup_expr='lte', widget=SelectDateWidget(years=CY))
    title = CharFilter(label='Title', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['created_after', 'created_before', 'title', 'author__user', 'cats']

