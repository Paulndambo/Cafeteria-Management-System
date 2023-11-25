import csv
import io  # Import the io module
import json
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.students.models import Student, StudentWallet, WalletRechargeLog
from apps.users.models import User

date_today = datetime.now().date()
# Create your views here.
def students_finder(request):
    students = Student.objects.all().order_by("-created")
    return render(request, "students_finder.html", {"students": students})

@login_required(login_url="/users/login/")
def students(request):
    students = Student.objects.all().order_by("-created")

    if request.method == "POST":
        registration_number = request.POST.get("reg_number")

        students = Student.objects.filter(
            Q(registration_number__icontains=registration_number) | 
            Q(user__id_number__icontains=registration_number) |
            Q(user__first_name__icontains=registration_number) |
            Q(user__last_name__icontains=registration_number) |
            Q(user__username__icontains=registration_number)
        ).order_by("-created")
    
    paginator = Paginator(students, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "students": students,
        "page_obj": page_obj
    }
    return render(request, "students/students.html", context)


@login_required(login_url="/users/login/")
def activate_deactivate_student(request, student_id=None):
    student = Student.objects.get(id=student_id)
    if student.status == "Active":
        student.status = "Deactivated"
    elif student.status == "Deactivated":
        student.status = "Active"
    student.save()
    return redirect("students")


@login_required(login_url="/users/login/")
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


@login_required(login_url="/users/login/")
@transaction.atomic
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
            print("User with this email found in the system")
            print(username, email, first_name, last_name)
        elif user_by_username:
    
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
                balance=350 if student_type == "Boarder" else 0,
                total_spend_today=0
            )

            messages.success(request, f"User created successfully!!")

        return redirect('students')

    return render(request, "modals/new_student.html")


@login_required(login_url="/users/login/")
def student_wallets(request):
    wallets = StudentWallet.objects.all()

    if request.method == "POST":
        reg_number = request.POST.get("reg_number")
        wallets = StudentWallet.objects.filter(
            Q(student__registration_number__icontains=reg_number) |
            Q(student__user__id_number__icontains=reg_number) |
            Q(student__user__first_name__icontains=reg_number) |
            Q(student__user__last_name__icontains=reg_number)
        )

    paginator = Paginator(wallets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "wallets": wallets,
        "page_obj": page_obj
    }
    return render(request, "students/student_wallets.html", context)


@login_required(login_url="/users/login/")
def recharge_student_wallet(request):
    if request.method == "POST":
        reg_number = request.POST.get("reg_number")
        recharge_method = request.POST.get("recharge_method")

        student = Student.objects.filter(
            Q(registration_number=reg_number) | Q(user__id_number=reg_number)).first()

        amount = Decimal(request.POST.get("amount"))

        wallet = student.studentwallet
        wallet.balance += amount
        wallet.save()

        recharge_log = WalletRechargeLog.objects.create(
            student=student,
            wallet=wallet,
            recharge_method=recharge_method,
            amount_recharged=amount
        )
        return redirect("student-wallets")

    return render(request, "modals/request_recharge.html")


@login_required(login_url="/users/login/")
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


@login_required(login_url="/users/login/")
def generate_daily_quota(request):
    student_wallets = StudentWallet.objects.filter(
        student__student_type="Boarder", student__status="Active").exclude(modified__date=date_today)

    if not student_wallets:
        print("Quotas for all students for today have been generated!!!")
        return redirect("student-wallets")

    for student_wallet in student_wallets:
        print(f"Student: {student_wallet.student}, Status: {student_wallet.student.status}, Student Type: {student_wallet.student.student_type}")
        student_wallet.total_spend_today = 0

        if student_wallet.student.status == "Deactivated":
            student_wallet.balance = 0
            student_wallet.save()
        else:
            student_wallet.balance = 350
            student_wallet.save()
    # print(student_wallets)
    return redirect("student-wallets")


def handle_uploaded_file(file):
    # Process the uploaded file (example: read CSV data)
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string)
    
    data = [row for row in reader]

    keys = data[0]

    # Create a list of dictionaries using the remaining sub-lists as values
    return [dict(zip(keys, values)) for values in data[1:]]
   

def upload_students(request):
    if request.method == "POST":
        
        res = handle_uploaded_file(request.FILES['student_file'])

        students_list = []
        for x in res:
            user = User.objects.filter(id_number=x.get('id_number')).first()

            if user:
                print("This Student Already Exists")
            else:
                user = User.objects.create(
                    first_name=x.get("first_name"),
                    last_name=x.get("last_name"),
                    email=x.get("email"),
                    username=x.get("id_number"),
                    id_number=x.get("id_number"),
                    role="student",
                    phone_number=x.get("phone_number"),
                    gender=x.get("gender")
                )

                student = Student.objects.create(
                    user=user,
                    student_type=x.get("student_type").capitalize(),
                    registration_number=x.get("reg_number"),
                    status=x.get("status"),
                    credit_limit=x.get("credit_limit")
                )
                wallet = StudentWallet.objects.create(
                    student=student,
                    balance = x.get("credit_limit") if x.get("status") == "Active" else 0
                )
                print("Student Created Successfully!!!!")

        return redirect("students")

        
    return render(request, "students/upload_students.html")


def student_details(request, student_id=None):
    student = Student.objects.get(id=student_id)
    orders = student.studentorders.all()

    paginator = Paginator(orders, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "student": student,
        "orders": orders,
        "page_obj": page_obj
    }
    return render(request, "students/student_details.html", context)



def search_student(request):
    if request.method == 'POST':
        reg_number = request.POST.get('reg_number')
        print(f"Student Reg. Number: {reg_number}")
        try:
            student = Student.objects.get(registration_number=reg_number)
            request.session['selected_student'] = {
                'id': student.id,
                'name': student.user.first_name,
                'wallet_balance': str(student.wallet_balance),
            }
            selected_student = request.session.get('selected_student')
            print(f"Selected Student: {student.user.first_name} {student.user.last_name}")
            return redirect('customer-order')
        except Student.DoesNotExist:
            # Handle the case when the student is not found
            pass

    return redirect("customer-order")