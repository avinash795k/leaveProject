from django.db import models
from django.contrib.auth.models import User



# Create your models here.

def user_return(self):
    return self.username+" "+self.first_name

User.add_to_class("__str__", user_return)


leave_choice=(
    ("CL","Casual Leave"),
    ("RH","Restricted Holidays"),
    ("SCL","Special Casual Leave"),
    ("EL","Earned Leave"),
    ("COL","Commuted Leave"),
    ("VL","Vacation Leave")
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
    station_add = models.CharField(max_length=300, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    purpose = models.CharField(max_length=300, default='')
    acad_duty = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="acad_duty")
    administrative_duty = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administrative_duty")
    remarks = models.CharField(max_length=200, default='')
    acad_tag = models.BooleanField(default=False)
    administrative_tag = models.BooleanField(default=False)
    forwarding_tag = models.BooleanField(default=False)
    sanctioning_tag = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.leave_emp.username)+" "+self.leave_emp.first_name+" "+str(self.cur_date)


class LeaveNotifier(models.Model):
    leavenotifier_emp = models.ForeignKey(User, on_delete=models.CASCADE)
    leavenotifier_leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    leavenotifier_type = models.CharField(max_length=20, choices=leavenotifier_choice)

    def __str__(self):
        return self.leavenotifier_emp.username+" "+self.leavenotifier_emp.first_name+" "+str(self.leavenotifier_leave.id)+" "+self.leavenotifier_type


class LeaveStatus(models.Model):
    leavestatus_emp = models.ForeignKey(User, on_delete=models.CASCADE)
    leavestatus_leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    leavestatus_status = models.BooleanField()

    def __str__(self):
        return self.leavestatus_emp.username+" "+self.leavestatus_emp.first_name+" "+str(self.leavestatus_leave.id)


class OngoingLeave(models.Model):
    ongoingleave_leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.ongoingleave_leave.leave_emp.username)+" "+self.ongoingleave_leave.leave_emp.first_name+" "+str(self.ongoingleave_leave.cur_date)

class LeaveRemaining(models.Model):
    leaveremaining_emp = models.OneToOneField(User, on_delete=models.CASCADE)
    leaveremaining_CL = models.IntegerField(default=8)
    leaveremaining_RH =models.IntegerField(default=2)
    leaveremaining_SCL = models.IntegerField(default=15)
    leaveremaining_EL = models.IntegerField(default=30)
    leaveremaining_COL = models.IntegerField(default=20)
    leaveremaining_VL = models.IntegerField(default=60)

    def __str__(self):
        return self.leaveremaining_emp.username+" "+self.leaveremaining_emp.first_name


class RestrictedHoliday(models.Model):
    holiday = models.CharField(max_length=100)
    holiday_date = models.DateField()
    holiday_year = models.IntegerField()

    def __str__(self):
        return  self.holiday


