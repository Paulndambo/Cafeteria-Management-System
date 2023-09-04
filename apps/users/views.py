from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from apps.users.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get("id_number")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        role = request.POST.get("role")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()


        if user_by_email:
            messages.error(request, f"User with this email exists already, try a different email!!")

        elif user_by_username:
            messages.error(request, f"User with this username exists already, try a different username!!")

            print(username, email, first_name, last_name)
        else:
            user = User.objects.create(
                first_name=first_name, 
                last_name=last_name, 
                username=username,
                email=email,
                role=role,
                gender=gender,
                phone_number=phone_number,
                id_number=id_number
            )
            user.set_password("1234")
            user.save()
            messages.success(request, f"User created successfully!!")

            return redirect('staff')
    
    
    return render(request, 'modals/new_staff.html',)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def staff(request):
    staffs = User.objects.filter(role__in=["chef", "admin", "cashier"])
    context = {
        "staffs": staffs
    }
    return render(request, "accounts/staff.html", context)