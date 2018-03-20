from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



# Create your views here.

# Fisrt Page
@method_decorator(login_required,name='dispatch')
class IndexView(TemplateView):
    template_name = 'homepage_app/index.html'

# Finder App
@method_decorator(login_required,name='dispatch')
class FinderView(TemplateView):
    template_name = 'homepage_app/finder.html'

# Visualize App
@method_decorator(login_required,name='dispatch')
class VisualizeView(TemplateView):
    template_name = 'homepage_app/visualize.html'


# ABOUT DECORATING CLASSES
# https://docs.djangoproject.com/en/2.0/topics/class-based-views/intro/#decorating-the-class