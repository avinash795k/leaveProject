from django.shortcuts import render, redirect
from .forms import FormLeave
from .models import *
from userpanel.models import *
from datetime import date
from workdays import networkdays

# Create your views here.

def leave_request(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        current_date = date.today()
        expiaredcheck_leave = OngoingLeave.objects.all()
        for lv in expiaredcheck_leave:
            if lv.ongoingleave_leave.to_date<current_date:
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
            if lv.ongoingleave_leave.from_date<=current_date and lv.ongoingleave_leave.to_date>=current_date:
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

        form = FormLeave(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['from_date']
            end_date = form.cleaned_data['to_date']
            cur_date = date.today()
            all_notifierleave = LeaveStatus.objects.filter(leavestatus_emp=request.user)
            if start_date<cur_date or end_date<start_date:
                return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Imappropriate Leave Period"})
            for lv in all_notifierleave:
                max_start = max(lv.leavestatus_leave.from_date, start_date)
                min_end = min(lv.leavestatus_leave.to_date, end_date)
                if max_start<=min_end:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "This Leave Period is coinciding with already sanctioned or pending Leave"})
            if EmployeeType.objects.get(type_employee=request.user).type_type=='Faculty':
                if form.cleaned_data['acad_duty']==None:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error":"Fill the academic responibility"})
                if form.cleaned_data['station_leave']==True and form.cleaned_data['station_add']=='':
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error":"Fill the station address"})
                if form.cleaned_data['acad_duty']==request.user or form.cleaned_data['administrative_duty']==request.user:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Self replacement not Allowed"})
                total_leaveperiod=networkdays(start_date,end_date,[])
                if(form.cleaned_data['leave_type']=='CL'):
                    remaining_leaveperiod=request.user.leaveremaining.leaveremaining_CL
                elif (form.cleaned_data['leave_type'] == 'RH'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_RH
                elif (form.cleaned_data['leave_type'] == 'SCL'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_SCL
                elif (form.cleaned_data['leave_type'] == 'EL'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_EL
                elif (form.cleaned_data['leave_type'] == 'COL'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_COL
                else :
                    if start_date<date(cur_date.year,5,1) or end_date>date(cur_date.year,7,31):
                        return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Requested period is not in Vacation Leave Period"})
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_VL
                if total_leaveperiod>remaining_leaveperiod:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Only "+str(remaining_leaveperiod)+" "+form.cleaned_data['leave_type']+" remaining this year"})
                if (form.cleaned_data['leave_type'] == 'RH'):
                    s1={start_date,end_date}
                    s2=set()
                    total_rh=RestrictedHoliday.objects.filter(holiday_year=cur_date.year)
                    for rh in total_rh:
                        s2.add(rh.holiday_date)
                    if len(s1 and s2)!=len(s1):
                        return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Requested dates are not Restricted Holidays"})

                leave_form = form.save(commit=False)
                acad_duty = leave_form.acad_duty
                administrative_duty = leave_form.administrative_duty
                if acad_duty.employeeleavestatus.leave_status:
                    return render(request, 'leaveapp/leave_request.html',{"form": form, "error": acad_duty.username+" "+acad_duty.first_name+" already on leave"})
                if administrative_duty.employeeleavestatus.leave_status:
                    return render(request, 'leaveapp/leave_request.html',{"form": form, "error": administrative_duty.usrname+" "+administrative_duty.first_name+" already on leave"})
                leave_form.leave_emp=request.user
                user_post = request.user.employeeleaveseeking.tempseeking_post
                if user_post.leaveforwarding_post == user_post.leavesanctioning_post:
                    leave_form.forwarding_tag = True
                if leave_form.leave_type == 'CL' or leave_form.leave_type == 'RH':
                    leave_form.forwarding_tag = True
                leave_form.save()
                LeaveNotifier.objects.create(leavenotifier_emp=leave_form.acad_duty, leavenotifier_leave=leave_form, leavenotifier_type='acad')
                LeaveNotifier.objects.create(leavenotifier_emp=leave_form.administrative_duty, leavenotifier_leave=leave_form, leavenotifier_type='administrative')
                LeaveStatus.objects.create(leavestatus_emp=request.user, leavestatus_leave=leave_form, leavestatus_status=False)

            else:
                if form.cleaned_data['station_leave'] == True and form.cleaned_data['station_add'] == '':
                    return render(request, 'leaveapp/leave_request.html',{"form": form, "error": "Fill the station address"})
                if form.cleaned_data['acad_duty']==request.user or form.cleaned_data['administrative_duty']==request.user:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Self replacement not Allowed"})
                total_leaveperiod = networkdays(start_date, end_date, [])
                if (form.cleaned_data['leave_type'] == 'VL'):
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Staff Can't apply for Vacation Leave "})
                elif (form.cleaned_data['leave_type'] == 'RH'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_RH
                elif (form.cleaned_data['leave_type'] == 'SCL'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_SCL
                elif (form.cleaned_data['leave_type'] == 'EL'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_EL
                elif (form.cleaned_data['leave_type'] == 'COL'):
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_COL
                else:
                    remaining_leaveperiod = request.user.leaveremaining.leaveremaining_CL
                if total_leaveperiod > remaining_leaveperiod:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Only " + str(remaining_leaveperiod) + " " + form.cleaned_data['leave_type'] + " remaining this year"})
                if (form.cleaned_data['leave_type'] == 'RH'):
                    s1={start_date,end_date}
                    s2=set()
                    total_rh=RestrictedHoliday.objects.filter(holiday_year=cur_date.year)
                    for rh in total_rh:
                        s2.add(rh.holiday_date)
                    if len(s1 and s2)!=len(s1):
                        return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Requested dates are not Restricted Holidays"})

                leave_form = form.save(commit=False)
                administrative_duty = leave_form.administrative_duty
                if administrative_duty.employeeleavestatus.leave_status:
                    return render(request, 'leaveapp/leave_request.html', {"form": form, "error": administrative_duty.usrname + " " + administrative_duty.first_name + " already on leave"})
                leave_form.leave_emp = request.user
                leave_form.acad_duty = True
                user_post = request.user.employeeleaveseeking.tempseeking_post
                if user_post.leaveforwarding_post == user_post.leavesanctioning_post:
                    leave_form.forwarding_tag = True
                if user_post.leaveforwarding_post == user_post.leavesanctioning_post:
                    leave_form.forwarding_tag = True
                if leave_form.leave_type == 'CL' or leave_form.leave_type == 'RH':
                    leave_form.forwarding_tag = True
                leave_form.save()
                LeaveNotifier.objects.create(leavenotifier_emp=leave_form.administrative_duty, leavenotifier_leave=leave_form,leavenotifier_type='administrative')
                LeaveStatus.objects.create(leavestatus_emp=request.user, leavestatus_leave=leave_form,leavestatus_status=False)

        return redirect('/leave_status')
    else:
        form = FormLeave()
        return render(request, 'leaveapp/leave_request.html', {"form": form})


def leave_status(request):
    if not request.user.is_authenticated():
        return redirect('/')
    leave_form = LeaveStatus.objects.filter(leavestatus_emp=request.user)
    return render(request, 'leaveapp/leave_status.html', {"leave_form":leave_form})


def leave_balance(request):
    if not request.user.is_authenticated():
        return redirect('/')
    remaining_lv = LeaveRemaining.objects.get(leaveremaining_emp=request.user)
    return render(request, 'leaveapp/balance_leave.html', {"remaining_lv":remaining_lv})



