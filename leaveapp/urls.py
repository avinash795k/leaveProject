from django.conf.urls import url
from . import views

app_name='leaveapp'
urlpatterns = [
    url(r'^leave_request$', views.leave_request, name='leave_request'),
    url(r'^leave_status$', views.leave_status, name='leave_status'),
    url(r'^leave_balance$', views.leave_balance, name='leave_balance'),
]
