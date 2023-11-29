from django.shortcuts import render,redirect,get_object_or_404
from .models import ExCustomer
from django.http import JsonResponse
from django.core.paginator import Paginator
# views.py
from .forms import ExCustomerForm  # Import your ExCustomerForm

from app1.models import Employee ,ProductType # Import your Employee model
from event.models import EventType  # Import your EventType model
# Create your views here.

def exform(request):
    state_choices = ExCustomer.STATE_CHOICES
    context = {
        'state_choices': state_choices,
    }
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        state = request.POST.get('state')
        customer_status = request.POST.get('customer') 
        ExCustomer.objects.create(
            first_name=first_name,
            state=state,
            customer_status=customer_status,
        )
        response_data = {'success': True}
        return JsonResponse(response_data)
    return render(request,'excustomer/excustomerform.html',context)

def ex_customer_reports(request):
    reports = ExCustomer.objects.all()
    reports = reports.order_by('-date_of_enquiry')
    employees = Employee.objects.all()
    events = EventType.objects.all()
    products=ProductType.objects.all()
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'reports': reports,
        'page_obj': page_obj,
        'employees': employees,
        'events': events,
        'products':products,}
    return render(request, 'excustomer/excustomer_reports.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import ExCustomerForm
from .models import ExCustomer

def edit_excustomer(request, pk):
    ex_customer = get_object_or_404(ExCustomer, pk=pk)

    if request.method == 'POST':
        form = ExCustomerForm(request.POST, instance=ex_customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form edited successfully')  # Add a success message
            return JsonResponse({'success': True})  # Return JSON response indicating success
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

    else:  # GET request or initial rendering
        form = ExCustomerForm(instance=ex_customer)

    context = {
        'form': form,
    }

    return render(request, 'excustomer/excustomer_reports.html', context)
