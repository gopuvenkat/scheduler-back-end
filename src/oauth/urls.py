from django.conf.urls import url
from oauth import views
from rest_framework.authtoken import views as rest_framework_views

app_name = "oauth"

urlpatterns = [
    # '/oauth'
    url(r'^$', views.home.as_view(), name = "home"),
    # explicit "/oauth/home"
    url(r'^home/$', views.home.as_view(), name = "home"),
    # 'oauth/gettoken'
    url(r'^gettoken/$', views.gettoken, name = "gettoken"),
    # 'oauth/mail'
    url(r'^mail/$', views.mailView.as_view(), name = "mail"),
    # 'oauth/token'
    url(r'^token/$', views.tokenView.as_view(), name = "token")
]
