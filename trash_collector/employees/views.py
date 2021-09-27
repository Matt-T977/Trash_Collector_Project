from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date

from .models import Employee

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    logged_in_user = request.user

    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()

        context = {
            'logged_in_employee' : logged_in_employee,
            'today' : today
        }
        return render(request, 'employees/index.html', context)

    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
   
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
