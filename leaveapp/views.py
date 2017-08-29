from django.shortcuts import render, redirect
from .forms import FormLeave

# Create your views here.

def leave_request(request):
    if not request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            form = FormLeave(request.POST)
            if not form.is_valid():
                return render(request, 'leaveapp/leave_request.html', {"form": form})
            #     username = request.POST.get("username")
            #     password = request.POST.get("password")
            #     user = authenticate(request, username=username, password=password)
            #     if user is not None:
            #         login(request, user)
            #         return redirect('/home')
            form = FormLeave()
            return render(request, 'leaveapp/leave_request.html', {"form": form, "error": "Invalid Username or Password"})
        else:
            form = FormLeave()
            return render(request, 'leaveapp/leave_request.html', {"form": form})
    # return render(request, 'leaveapp/leave_request.html')


