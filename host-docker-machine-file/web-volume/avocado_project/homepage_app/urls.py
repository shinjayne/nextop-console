from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns=[
    #url(r'^tasks/',views.tasks, name="tasks"),
    url(r'^$', views.IndexView.as_view(), name="homepage_index"),
    url(r'^finder/$',views.FinderView.as_view(), name="homepage_finder"),
    url(r'^visualize/$',views.VisualizeView.as_view(),name="homepage_visualize"),
]
