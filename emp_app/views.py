from django.shortcuts import render,HttpResponse
from .models import Department, Role, Employee
from datetime import datetime
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps,
    }
    return render(request, "all_emp.html", context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = int(request.POST['role'])
        phone = request.POST['phone']
        hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d').date()

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            dept_id=dept,
            salary=salary,
            bonus=bonus,
            role_id=role,
            phone=phone,
            hire_date=hire_date
        )
        new_emp.save()
        return HttpResponse("Employee Added Successfully")
    elif request.method=="GET":
        return render(request, "add_emp.html")
    else:
        return HttpResponse("An Exceptional Occured in Employee")
    

def remove_emp(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        phone = request.POST.get('phone')

        if emp_id:
            try:
                emp_to_be_removed = Employee.objects.get(id=emp_id)
                emp_to_be_removed.delete()
                return HttpResponse("Employee removed successfully")
            except Employee.DoesNotExist:
                return HttpResponse("Invalid Employee ID. Please enter a valid Employee ID.")
        elif phone:
            try:
                emp_to_be_removed = Employee.objects.get(phone=phone)
                emp_to_be_removed.delete()
                return HttpResponse("Employee removed successfully")
            except Employee.DoesNotExist:
                return HttpResponse("Invalid Phone Number. Please enter a valid Phone Number.")
    
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, "remove_emp.html", context)


def filter_emp(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        
        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An Exception Occurred")