from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Department)
admin.site.register(EmployeeDepartment)
admin.site.register(EmployeeType)
admin.site.register(AllPost)
admin.site.register(LeaveauthorityPost)
admin.site.register(LeaveseekingPost)
admin.site.register(EmployeeLeaveseeking)
admin.site.register(EmployeeLeaveauthority)
admin.site.register(EmployeeLeavestatus)
admin.site.register(EmployeeAllpost)
admin.site.register(ReplacingEmployee)