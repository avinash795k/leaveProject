from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from leaveapp.models import *
from .models import *
from datetime import date
from workdays import networkdays

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/')
    current_date = date.today()
    expiaredcheck_leave = OngoingLeave.objects.all()
    for lv in expiaredcheck_leave:
        if lv.ongoingleave_leave.to_date < current_date:
            lv.ongoingleave_leave.leave_emp.employeeleavestatus.leave_status = False
            lv.ongoingleave_leave.leave_emp.employeeleavestatus.save()
            lv.ongoingleave_leave.administrative_duty.employeeleaveseeking.tempseeking_post = lv.ongoingleave_leave.administrative_duty.employeeleaveseeking.seeking_post
            lv.ongoingleave_leave.administrative_duty.employeeleaveseeking.save()
            try:
                lv.ongoingleave_leave.leave_emp.replacingemployee.delete()
            except:
                pass
            lv.delete()
    for lv in expiaredcheck_leave:
        if lv.ongoingleave_leave.from_date <= current_date and lv.ongoingleave_leave.to_date >= current_date:
            lv.ongoingleave_leave.leave_emp.employeeleavestatus.leave_status = True
            lv.ongoingleave_leave.leave_emp.employeeleavestatus.save()
            passing_post = lv.ongoingleave_leave.leave_emp.employeeleaveseeking.tempseeking_post
            gaining_emp = lv.ongoingleave_leave.administrative_duty
            if passing_post.leaveseeking_post.post == gaining_emp.employeeleaveseeking.tempseeking_post.leaveforwarding_post.leaveauthority_post.post or passing_post.leaveseeking_post.post == gaining_emp.employeeleaveseeking.tempseeking_post.leavesanctioning_post.leaveauthority_post.post:
                gaining_emp.employeeleaveseeking.tempseeking_post = passing_post
                gaining_emp.employeeleaveseeking.save()
            try:
                lv.ongoingleave_leave.leave_emp.replacingemployee.replacing_administrative = lv.ongoingleave_leave.administrative_duty
                lv.ongoingleave_leave.leave_emp.replacingemployee.replacing_academic = lv.ongoingleave_leave.acad_duty
                lv.ongoingleave_leave.leave_emp.replacingemployee.save()
            except:
                ReplacingEmployee.objects.create(
                    replacing_employee=lv.ongoingleave_leave.leave_emp,
                    replacing_academic=lv.ongoingleave_leave.acad_duty,
                    replacing_administrative=lv.ongoingleave_leave.administrative_duty
                )
    if request.method=='POST':
        r_id=request.POST.get('request_id')
        process_leave = LeaveNotifier.objects.get(id=r_id)
        if request.POST.get('submit') == 'Accept' or request.POST.get('submit') == 'Forward':
            if process_leave.leavenotifier_type == 'acad':
                process_leave.leavenotifier_leave.acad_tag = True
                process_leave.leavenotifier_leave.remarks = "[Academic Duty Accepted by "+str(request.user)+"] "+request.POST.get('remarks')
                process_leave.leavenotifier_leave.save()
                if process_leave.leavenotifier_leave.administrative_tag:
                    if process_leave.leavenotifier_leave.forwarding_tag:
                        emp = process_leave.leavenotifier_leave.leave_emp.employeeleaveseeking.tempseeking_post.leaveforwarding_post.employeeleaveauthority.authority_employee
                        if emp.employeeleavestatus.leave_status:
                            emp = ReplacingEmployee.objects.get(replacing_employee=emp).replacing_administrative
                        LeaveNotifier.objects.create(
                            leavenotifier_emp=emp,
                            leavenotifier_leave=process_leave.leavenotifier_leave,
                            leavenotifier_type='sanctioning')
                    else:
                        emp = process_leave.leavenotifier_leave.leave_emp.employeeleaveseeking.tempseeking_post.leaveforwarding_post.employeeleaveauthority.authority_employee
                        if emp.employeeleavestatus.leave_status:
                            emp = ReplacingEmployee.objects.get(replacing_employee=emp).replacing_administrative
                        LeaveNotifier.objects.create(
                            leavenotifier_emp=emp,
                            leavenotifier_leave=process_leave.leavenotifier_leave,
                            leavenotifier_type='forwarding')

            elif process_leave.leavenotifier_type == 'administrative':
                process_leave.leavenotifier_leave.administrative_tag = True
                process_leave.leavenotifier_leave.remarks = "[Administrative Duty Accepted by "+str(request.user)+"] " + request.POST.get('remarks')
                process_leave.leavenotifier_leave.save()
                if process_leave.leavenotifier_leave.acad_tag:
                    if process_leave.leavenotifier_leave.forwarding_tag:
                        emp = process_leave.leavenotifier_leave.leave_emp.employeeleaveseeking.tempseeking_post.leaveforwarding_post.employeeleaveauthority.authority_employee
                        if emp.employeeleavestatus.leave_status:
                            emp = ReplacingEmployee.objects.get(replacing_employee=emp).replacing_administrative
                        LeaveNotifier.objects.create(
                            leavenotifier_emp=emp,
                            leavenotifier_leave=process_leave.leavenotifier_leave,
                            leavenotifier_type='sanctioning')
                    else:
                        emp = process_leave.leavenotifier_leave.leave_emp.employeeleaveseeking.tempseeking_post.leaveforwarding_post.employeeleaveauthority.authority_employee
                        if emp.employeeleavestatus.leave_status:
                            emp = ReplacingEmployee.objects.get(replacing_employee=emp).replacing_administrative
                        LeaveNotifier.objects.create(
                            leavenotifier_emp=emp,
                            leavenotifier_leave=process_leave.leavenotifier_leave,
                            leavenotifier_type='forwarding')

            elif process_leave.leavenotifier_type == 'forwarding':
                process_leave.leavenotifier_leave.forwarding_tag = True
                process_leave.leavenotifier_leave.remarks = "[Leave Forwarded by "+str(request.user)+"] " + request.POST.get('remarks')
                process_leave.leavenotifier_leave.save()
                emp = process_leave.leavenotifier_leave.leave_emp.employeeleaveseeking.tempseeking_post.leavesanctioning_post.employeeleaveauthority.authority_employee
                if emp.employeeleavestatus.leave_status:
                    emp = ReplacingEmployee.objects.get(replacing_employee=emp).replacing_administrative
                LeaveNotifier.objects.create(
                    leavenotifier_emp=emp,
                    leavenotifier_leave=process_leave.leavenotifier_leave,
                    leavenotifier_type='sanctioning'
                )

            else:
                process_leave.leavenotifier_leave.sanctioning_tag = True
                process_leave.leavenotifier_leave.status = True
                process_leave.leavenotifier_leave.remarks = "[Leave Sanctioned by "+str(request.user)+"] " + request.POST.get('remarks')
                process_leave.leavenotifier_leave.save()
                object_leavestatus = LeaveStatus.objects.get(leavestatus_leave=process_leave.leavenotifier_leave)
                object_leavestatus.leavestatus_status = True
                object_leavestatus.save()
                OngoingLeave.objects.create(ongoingleave_leave=process_leave.leavenotifier_leave)
                start_date = process_leave.leavenotifier_leave.from_date
                end_date = process_leave.leavenotifier_leave.to_date
                total_leaveperiod = networkdays(start_date, end_date, [])
                if (process_leave.leavenotifier_leave.leave_type == 'CL'):
                    process_leave.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_CL -= total_leaveperiod
                elif (process_leave.leavenotifier_leave.leave_type == 'RH'):
                    process_leave.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_RH -= total_leaveperiod
                elif (process_leave.leavenotifier_leave.leave_type == 'SCL'):
                    process_leave.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_SCL -= total_leaveperiod
                elif (process_leave.leavenotifier_leave.leave_type == 'EL'):
                    process_leave.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_EL -= total_leaveperiod
                elif (process_leave.leavenotifier_leave.leave_type == 'COL'):
                    process_leave.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_COL -= total_leaveperiod
                else:
                    process_leave.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_VL -= total_leaveperiod
                process_leave.leavenotifier_leave.leave_emp.leaveremaining.save()

        else:
            if process_leave.leavenotifier_type == 'administrative' and not process_leave.leavenotifier_leave.acad_tag:
                LeaveNotifier.objects.get(leavenotifier_emp=process_leave.leavenotifier_leave.acad_duty, leavenotifier_leave=process_leave.leavenotifier_leave, leavenotifier_type='acad').delete()
            if process_leave.leavenotifier_type == 'acad' and not process_leave.leavenotifier_leave.administrative_tag:
                LeaveNotifier.objects.get(leavenotifier_emp=process_leave.leavenotifier_leave.administrative_duty, leavenotifier_leave=process_leave.leavenotifier_leave, leavenotifier_type='administrative').delete()
            process_leave.leavenotifier_leave.status = True
            if process_leave.leavenotifier_type == 'acad':
                process_leave.leavenotifier_leave.remarks = "[Administrative Duty Denied by " + str(request.user) + "] " + request.POST.get('remarks')
            elif process_leave.leavenotifier_type == 'administrative':
                process_leave.leavenotifier_leave.remarks = "[Administrative Duty Denied by " + str(request.user) + "] " + request.POST.get('remarks')
            elif process_leave.leavenotifier_type == 'forwarding':
                process_leave.leavenotifier_leave.remarks = "[Leave Forwarding Denied by " + str(request.user) + "] " + request.POST.get('remarks')
            else:
                process_leave.leavenotifier_leave.remarks = "[Leave Sanctioned by " + str(request.user) + "] " + request.POST.get('remarks')
            process_leave.leavenotifier_leave.save()


        process_leave.delete()

    leave_request = LeaveNotifier.objects.filter(leavenotifier_emp=request.user)
    for each_leaverequest in leave_request:
        start_date = each_leaverequest.leavenotifier_leave.from_date
        end_date = each_leaverequest.leavenotifier_leave.to_date
        total_leaveperiod = networkdays(start_date, end_date, [])
        if (each_leaverequest.leavenotifier_leave.leave_type == 'CL'):
            remaining_leaveperiod = each_leaverequest.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_CL
        elif (each_leaverequest.leavenotifier_leave.leave_type == 'RH'):
            remaining_leaveperiod = each_leaverequest.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_RH
        elif (each_leaverequest.leavenotifier_leave.leave_type == 'SCL'):
            remaining_leaveperiod = each_leaverequest.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_SCL
        elif (each_leaverequest.leavenotifier_leave.leave_type == 'EL'):
            remaining_leaveperiod = each_leaverequest.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_EL
        elif (each_leaverequest.leavenotifier_leave.leave_type == 'COL'):
            remaining_leaveperiod = each_leaverequest.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_COL
        else:
            remaining_leaveperiod = each_leaverequest.leavenotifier_leave.leave_emp.leaveremaining.leaveremaining_VL

        print(total_leaveperiod,remaining_leaveperiod)
        if total_leaveperiod > remaining_leaveperiod:
            if each_leaverequest.leavenotifier_type == 'administrative' and not each_leaverequest.leavenotifier_leave.acad_tag:
                LeaveNotifier.objects.get(leavenotifier_emp=each_leaverequest.leavenotifier_leave.acad_duty,
                                          leavenotifier_leave=each_leaverequest.leavenotifier_leave,
                                          leavenotifier_type='acad').delete()
            if each_leaverequest.leavenotifier_type == 'acad' and not each_leaverequest.leavenotifier_leave.administrative_tag:
                LeaveNotifier.objects.get(leavenotifier_emp=each_leaverequest.leavenotifier_leave.administrative_duty,
                                          leavenotifier_leave=each_leaverequest.leavenotifier_leave,
                                          leavenotifier_type='administrative').delete()
            each_leaverequest.leavenotifier_leave.status = True
            each_leaverequest.leavenotifier_leave.remarks = "Insufficient Leave"
            each_leaverequest.leavenotifier_leave.save()
            each_leaverequest.delete()
    leave_request = LeaveNotifier.objects.filter(leavenotifier_emp=request.user)
    return render(request, 'userpanel/home.html', {"leave_request": leave_request})



def login_user(request):
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method=='POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/home')
        form = FormLogin()
        return render(request, 'userpanel/login_page.html', {"form":form,"error":"Invalid Username or Password"})
    else:
        form = FormLogin()
        return render(request, 'userpanel/login_page.html', {"form":form})


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')