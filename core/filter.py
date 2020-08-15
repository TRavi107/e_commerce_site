import django_filters
from .models import Items,CATEGORIES_CHOICES

class ItemsFilter(django_filters.FilterSet):
    model = Items
    """ordering = django_filters.ChoiceFilter(
        label='Categories',
        choices = CATEGORIES_CHOICES,
        method = 'sort_by_categories'
    )"""
    title = django_filters.CharFilter(
        #Customize the search bar design
        lookup_expr = 'icontains'
    )

    def sort_by_categories(self,queryset,name,value):
        return queryset.filter(categories=value[0])

