from django.conf.urls import url
from . import views

app_name='userpanel'
urlpatterns = [
    url(r'^home$', views.home, name='home' ),
    url(r'^$', views.login_user, name='login_user' ),
    url(r'^logout$', views.logout_user, name='logout_user'),
]
