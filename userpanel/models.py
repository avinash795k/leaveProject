from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_return(self):
    return self.username+" "+self.first_name

User.add_to_class("__str__", user_return)




class Department(models.Model):
    dept = models.CharField(max_length=100)

    def __str__(self):
        return self.dept

class EmployeeDepartment(models.Model):
    dept_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    dept_department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.dept_employee.username+" "+self.dept_employee.first_name+" "+self.dept_department.dept


class EmployeeType(models.Model):
    type_employee = models.OneToOneField(User, on_delete=models.CASCADE)
    type_type = models.CharField(max_length=10, choices=(("Staff","Staff"),("Faculty","Faculty")))

    def __str__(self):
        return self.type_employee.username+" "+self.type_employee.first_name



class AllPost(models.Model):
    post = models.CharField(max_length=200)

    def __str__(self):
        return self.post


class LeaveauthorityPost(models.Model):
    leaveauthority_post = models.ForeignKey(AllPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.leaveauthority_post.post


class LeaveseekingPost(models.Model):
    leaveseeking_post = models.ForeignKey(AllPost, on_delete=models.CASCADE)
    leaveforwarding_post = models.ForeignKey(LeaveauthorityPost, on_delete=models.CASCADE, related_name="forwarding")
    leavesanctioning_post = models.ForeignKey(LeaveauthorityPost, on_delete=models.CASCADE, related_name="sanctioning")

    def __str__(self):
        return self.leaveseeking_post.post


class EmployeeLeaveseeking(models.Model):
    seeking_employee = models.OneToOneField(User, on_delete=models.CASCADE)
    seeking_post = models.ForeignKey(LeaveseekingPost, on_delete=models.CASCADE)
    tempseeking_post = models.ForeignKey(LeaveseekingPost, on_delete=models.CASCADE, related_name='temp_post')

    def __str__(self):
        return self.seeking_employee.username+" "+self.seeking_employee.first_name


class EmployeeLeaveauthority(models.Model):
    authority_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    authority_post = models.OneToOneField(LeaveauthorityPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.authority_post.leaveauthority_post.post


class EmployeeLeavestatus(models.Model):
    leave_employee = models.OneToOneField(User, on_delete=models.CASCADE)
    leave_status = models.BooleanField(default=False)

    def __str__(self):
        return self.leave_employee.username+" "+self.leave_employee.first_name


class EmployeeAllpost(models.Model):
    post_employee = models.ForeignKey(User, on_delete=models.CASCADE)
    post_post = models.ForeignKey(AllPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_employee.username+" "+self.post_employee.first_name+" "+self.post_post.post


class ReplacingEmployee(models.Model):
    replacing_employee = models.OneToOneField(User, on_delete=models.CASCADE )
    replacing_academic = models.ForeignKey(User, on_delete=models.CASCADE, related_name="academic", null=True)
    replacing_administrative = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administrative")

    def __str__(self):
        return self.replacing_employee.username+" "+self.replacing_employee.first_name


