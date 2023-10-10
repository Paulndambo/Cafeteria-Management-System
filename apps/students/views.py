from decimal import Decimal
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.students.models import Student, StudentWallet
from apps.users.models import User

date_today = datetime.now().date()
# Create your views here.
def students(request):
    students = Student.objects.all().order_by("-created")
    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "students": students,
        "page_obj": page_obj
    }
    return render(request, "students/students.html", context)

def activate_deactivate_student(request, student_id=None):
    student = Student.objects.get(id=student_id)
    if student.status == "Active":
        student.status = "Deactivated"
    elif student.status == "Deactivated":
        student.status = "Active"
    student.save()
    return redirect("students")


def delete_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student = Student.objects.filter(id=student_id).first()
        if student:
            student.delete()
            return redirect("students")
        else:
            return messages.error(request, f"Student with id: {student_id} does not exist on the database")
    return render(request, "modals/students/delete_student.html")

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
            return messages.error(request, f"User with this email exists already, try a different email!!")
            print(username, email, first_name, last_name)
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


def recharge_student_wallet(request):
    if request.method == "POST":
        reg_number = request.POST.get("reg_number")

        student = Student.objects.filter(Q(registration_number=reg_number) | Q(user__id_number=reg_number)).first()

        amount = Decimal(request.POST.get("amount"))

        wallet = student.studentwallet
        wallet.balance += amount
        wallet.save()
        return redirect("student-wallets")

    return render(request, "modals/request_recharge.html")



def edit_student(request):
    if request.method == 'POST':
        try:
            student_id = request.POST.get("student_id")
            user_id = request.POST.get("user_id")

            if student_id and user_id:

                username = request.POST.get("username")
                email = request.POST.get("email")
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                gender = request.POST.get("gender")
                phone_number = request.POST.get("phone_number")
                id_number = request.POST.get("id_number")
                registration_number = request.POST.get("reg_number")
                student_type = request.POST.get("student_type")
                

                user = User.objects.get(id=user_id)
                student = Student.objects.get(id=student_id)
                
                user.first_name = first_name if first_name else user.first_name
                user.last_name = last_name if last_name else user.last_name
                user.email = email if email else user.email
                user.gender = gender if gender else user.gender
                user.phone_number = phone_number if phone_number else user.phone_number
                user.id_number = id_number if id_number else user.id_number
                user.username = username if username else user.username
                user.save()
                

                student.student_type = student_type if student_type else student.student_type
                
                student.registration_number = registration_number if registration_number else student.registration_number
                
                student.save()

                    
                messages.success(request, f"User updated successfully!!")

            return redirect('students')
        except Exception as e:
            raise e

    return render(request, "modals/students/edit_student.html")


def generate_daily_quota(request):
    student_wallets = StudentWallet.objects.filter(student__student_type="Boarder").exclude(modified__date=date_today)

    if not student_wallets:
        print("Quotas for all students for today have been generated!!!")
        return redirect("student-wallets")
        

    for student_wallet in student_wallets:
        student_wallet.total_spend_today = 0
        student_wallet.balance = 350
    StudentWallet.objects.bulk_update(student_wallets, ["total_spend_today", "balance"])

    return redirect("student-wallets")
