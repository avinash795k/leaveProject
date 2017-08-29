from django.db import models
from django.contrib.auth.models import User



# Create your models here.
leave_choice=(
    ("CL","Casual Leave"),
    ("RH","Restricted Holidays"),
    ("SCL","Special Casual Leave"),
    ("EL","Earned Leave"),
    ("COL","Commuted Leave")
)
leavenotifier_choice=(
    ("acad","Academic Responsibility"),
    ("administrative","Administrative Responsibility"),
    ("forwarding","Leave Forwarding"),
    ("sanctioning","Leave Sanctioning")
)

class Leave(models.Model):
    leave_emp = models.ForeignKey(User, on_delete=models.CASCADE)
    cur_date =models.DateTimeField(auto_now=True)
    leave_type = models.CharField(max_length=5, choices=leave_choice)
    station_leave = models.BooleanField(default=False)
    station_add = models.CharField(max_length=300, null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    acad_duty = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acad_duty")
    administrative_duty = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administrative_duty")
    acad_tag = models.BooleanField(default=False)
    administrative_tag = models.BooleanField(default=False)
    forwarding_tag = models.BooleanField(default=False)
    sanctioning_tag = models.BooleanField(default=False)
    status = models.BooleanField(default=False)


class LeaveNotifier(models.Model):
    leavenotifier_emp = models.ForeignKey(User, on_delete=models.CASCADE)
    leavenotifier_leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    leavenotifier_type = models.CharField(max_length=20, choices=leavenotifier_choice)


class LeaveStatus(models.Model):
    leavestatus_emp = models.ForeignKey(User, on_delete=models.CASCADE)
    leavestatus_leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    leavestatus_status = models.BooleanField()


class LeaveRemaining(models.Model):
    leaveremaining_emp = models.ForeignKey(User, on_delete=models.CASCADE)
    leaveremaining_CL = models.IntegerField()
    leaveremaining_RH =models.IntegerField()
    leaveremaining_SCL = models.IntegerField()
    leaveremaining_EL = models.IntegerField()
    leaveremaining_COL = models.IntegerField()


