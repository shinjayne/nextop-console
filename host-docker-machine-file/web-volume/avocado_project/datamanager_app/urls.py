from django.conf.urls import url

from . import views

# TODO : Restful 한 API 로 만들어서 Front / Back 분리 작업

# TODO : Data 조회 / 이상점 / 추가 페이지 만들기
urlpatterns=[
    url(r'^$', views.menu_view, name='datamanager_menu'),
    url(r'^overview/$', views.overview_view, name="datamanager_overview"),
    url(r'^warning/$', views.warning_view, name="datamanager_warning"),
    url(r'^list/(?P<m>[a-z]*)/(?P<page>[0-9]*)/$',views.list_view, name="datamanager_list"),
    url(r'^info/(?P<m>[a-z]*)/(?P<id>[0-9]*)/$', views.info_view, name="datamanager_info"),

    # backend api
    url(r'^api/chart/trend/$', views.chart_trend_api, name="datamanager_api_chart_trend"),
    url(r'api/chart/rhythm/$', views.chart_rhythm_api, name="datamanager_api_chart_rhythm"),
    url(r'api/chart/rhythm-plot/$', views.chart_rhythm_plot_api, name="datamanager_api_chart_rhythm_plot"),
    url(r'^api/chart/rank/$', views.chart_rank_api, name="datamanager_api_chart_rank"),
    url(r'^api/list/',views.list_api, name="datamanager_api_list"),

    # url(r'^upload/$', views.upload_view, name="datamanager_upload"),
]
