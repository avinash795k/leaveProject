from django.conf.urls import url
from . import views

app_name='leaveapp'
urlpatterns = [
    url(r'^leave_request$', views.leave_request, name='leave_request'),
]
