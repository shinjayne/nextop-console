from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^upload/$',views.upload, name="upload"),
    url(r'^shownow/$',views.shownow, name="shownow"),
    url(r'^showpredict/$',views.showpredict, name="showpredict"),
    url(r'^form/$',views.form, name="form"),
    url(r'^companyinfo/(?P<company_id>[0-9]+)/$',views.company_info, name="company_info"),
    url(r'^company/p=(?P<page_number>[0-9]+)/$', views.company, name='company'),

]
