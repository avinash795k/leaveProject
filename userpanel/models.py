from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    dept = models.CharField(max_length=100)

    def __str__(self):
        return self.dept

class EmployeeDepartment(models.Model):
    dept_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    dept_department = models.ForeignKey(Department, on_delete=models.CASCADE)


class EmployeeType(models.Model):
    type_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    type_type = models.CharField(max_length=10, choices=(("Staff","Staff"),("Faculty","Faculty")))



class AllPost(models.Model):
    post = models.CharField(max_length=200)

    def __str__(self):
        return self.post


class LeaveauthorityPost(models.Model):
    leaveauthority_post = models.ForeignKey(AllPost, on_delete=models.CASCADE)


class LeaveseekingPost(models.Model):
    leaveseeking_post = models.ForeignKey(AllPost, on_delete=models.CASCADE)
    leaveforwarding_post = models.ForeignKey(AllPost, on_delete=models.CASCADE, related_name="forwarding")
    leavesanctioning_post = models.ForeignKey(AllPost, on_delete=models.CASCADE, related_name="sanctioning")


class EmployeeLeaveseeking(models.Model):
    seeking_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    seeking_post = models.ForeignKey(LeaveseekingPost, on_delete=models.CASCADE)


class EmployeeLeaveauthority(models.Model):
    authority_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    authority_post = models.ForeignKey(LeaveauthorityPost, on_delete=models.CASCADE)


class EmployeeLeavestatus(models.Model):
    leave_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_status = models.BooleanField(default=False)


class EmployeeAllpost(models.Model):
    post_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    post_post = models.ForeignKey(AllPost, on_delete=models.CASCADE)


class ReplacingEmployee(models.Model):
    replacing_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    replacing_academic = models.ForeignKey(User, on_delete=models.CASCADE, related_name="academic", null=True)
    replacing_administrative = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administrative")


