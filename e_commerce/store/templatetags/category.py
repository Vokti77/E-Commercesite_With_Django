from django import template
from store.models import Category

register = template.Library()



@register.filter  # filter
def category(user):  # Find Authenticate user
    if user.is_authenticated:
        cat = Category.objects.filter(parent=None)  # Find all category, their has no parent category
        return cat  # Return list/array
