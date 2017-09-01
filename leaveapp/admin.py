from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Leave)
admin.site.register(LeaveNotifier)
admin.site.register(LeaveStatus)
admin.site.register(LeaveRemaining)
admin.site.register(OngoingLeave)