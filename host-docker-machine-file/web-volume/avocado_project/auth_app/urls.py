from django.conf.urls import url

from . import views


urlpatterns=[
    url(r"^login/$",views.loginview, name="auth_login"),
    url(r'^logout/$', views.logoutview, name = "auth_logout"),
]

# TODO : login/ GET method to get redirect_url in loginview
# TODO : 비밀번호 변경기능 추가
# TODO : 회원가입 기능 추가