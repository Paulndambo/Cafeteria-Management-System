from django.shortcuts import render, redirect
from django.contrib import messages

from apps.users.models import User
from apps.students.models import Student, StudentWallet

# Create your views here.
def students(request):
    students = Student.objects.all().order_by("-created")
    context = {
        "students": students
    }
    return render(request, "students/students.html", context)

def new_student(request):
    if request.method == 'POST':
        username = request.POST.get("id_number")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")
        registration_number = request.POST.get("reg_number")
        student_type = request.POST.get("student_type")

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
                role="student",
                gender=gender,
                phone_number=phone_number,
                id_number=id_number
            )
            user.set_password("1234")
            user.save()

            student = Student.objects.create(
                registration_number=registration_number,
                user=user,
                student_type=student_type,
                status="Active"
            )

            wallet = StudentWallet.objects.create(
                student=student,
                balance=300 if student_type == "Boarder" else 0,
                total_spend_today=0
            )


            messages.success(request, f"User created successfully!!")

            return redirect('students')

    return render(request, "modals/new_student.html")


def student_wallets(request):
    wallets = StudentWallet.objects.all()
    context = {
        "wallets": wallets
    }
    return render(request, "students/student_wallets.html", context)