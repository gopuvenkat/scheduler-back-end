from django.conf.urls import url
from oauth import views

app_name = "oauth"

urlpatterns = [
    # '/oauth'
    url(r'^$', views.home, name = "home"),
    # explicit "/oauth/home"
    url(r'^home/$', views.home, name = "home"),
    # 'oauth/gettoken'
    url(r'^gettoken/$', views.gettoken, name = "gettoken"),
    # 'oauth/mail'
    url(r'^mail/$', views.mail, name = "mail")
]
