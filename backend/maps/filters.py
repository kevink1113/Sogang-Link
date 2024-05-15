# filters.py
import django_filters
from .models import Restaurant
from django.db.models import Q


class RestaurantFilter(django_filters.FilterSet):
    all = django_filters.CharFilter(method='general_search', label='Search')

    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    place = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name="avg_Price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="avg_Price", lookup_expr='lte')
    tags = django_filters.CharFilter(method='filter_by_tags', label='Tags')

    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'place', 'min_price', 'max_price', 'tags', 'all']

    def general_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(address__icontains=value) |
            Q(place__icontains=value) |
            Q(OneLiner__icontains=value) |
            Q(tags__name__icontains=value)
        ).distinct()
        
    def filter_by_tags(self, queryset, name, value):
        return queryset.filter(tags__name__icontains=value).distinct()