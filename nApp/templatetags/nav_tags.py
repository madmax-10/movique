from django import template
from nApp.models import Genre  # replace with your actual model

register = template.Library()

@register.inclusion_tag('partials/nav_model_data.html')
def load_nav_data():
    data = Genre.objects.all()  # Add your preprocessing here
    return {'genres': data}