from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

from .models import Employee

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')

    logged_in_user = request.user

    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        day_of_the_week = datetime.weekday(today)
        day_of_the_week_string = day_of_the_week_to_string(day_of_the_week)
        customer_list = Customer.objects.all().filter(zip_code=logged_in_employee.zip_code).filter(weekly_pickup=day_of_the_week_string).exclude(suspend_end__gt=today , suspend_start__lt=today)
        one_time_pickup_customers = Customer.objects.all().filter(one_time_pickup=today)
        # customer_list = customer.objects.exclude()

        context = {
            'customer_list' : customer_list,
            'one_time_pickup_customers' : one_time_pickup_customers,
            'logged_in_employee' : logged_in_employee,
            'today' : today
        }
        return render(request, 'employees/index.html', context)

    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required   
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        phone_number_from_form = request.POST.get('phone_number')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form, phone_number=phone_number_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        phone_number_from_form = request.POST.get('phone_number')
        logged_in_employee.name = name_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.phone_number = phone_number_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

'''General Python Functions Below'''

def day_of_the_week_to_string(day_of_the_week):
    if day_of_the_week == 0:
        return 'Monday'
    elif day_of_the_week == 1:
        return 'Tuesday'
    elif day_of_the_week == 2:
        return 'Wednesday'
    elif day_of_the_week == 3:
        return 'Thursday'
    elif day_of_the_week == 4:
        return 'Friday'
    elif day_of_the_week == 5:
        return 'Saturday'
    else:
        return 'Sunday'

# def day_name(today):
#     day_dictionary = {
#         0 : 'Monday',
#         1 : 'Tuesday',
#         2 : 'Wednesday',
#         3 : 'Thursday',
#         4 : 'Friday',
#         5 : 'Saturday',
#         6 : 'Sunday'
#     }
#     for day in day_dictionary:
#         if day == today:
#             return day