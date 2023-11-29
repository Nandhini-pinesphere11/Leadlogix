from django.shortcuts import render,redirect
from .models import Vendor,DepartmentType
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from .forms import DepartmentForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def vendor(request):
    user = request.user  # Assuming the user is logged in
    enable_option = user.has_perm('vendor.can_view_vendor')
    vendors = Vendor.objects.filter(user=user)
    vendor_count = vendors.count()
    department_counts = vendors.values('department').annotate(count=Count('department')).order_by('-count')
    if department_counts:
        highest_department = department_counts[0]['department']
        highest_count = department_counts[0]['count']
    else:
        highest_department = None
        highest_count = 0

    # Count the occurrences of each state for the user's company and order them by count in descending order
    state_count = vendors.values('state').annotate(count=Count('state')).order_by('-count')

    # Get the state with the highest count for the user's company
    highest_state = state_count.first()
    highest_state_value = highest_state['state'] if highest_state else None
    highest_state_count = highest_state['count'] if highest_state else 0
     # Calculate state data for the user's company
    state_data = vendors.values('state').annotate(vendor_count=Count('state')).order_by('-vendor_count')

    total_vendors = vendors.count()

    # Calculate the progress_percentage for each state based on its count for the user's company
    for state in state_data:
        state['progress_percentage'] = (state['vendor_count'] / total_vendors) * 100 if total_vendors > 0 else 0

    department_data = vendors.exclude(department__isnull=True).values('department').annotate(vendor_count=Count('department')).order_by('-vendor_count')
    
    for department in department_data:
        department['progress_percentage'] = (department['vendor_count'] / total_vendors) * 100 if total_vendors > 0 else 0

    true_same_industry_count = vendors.filter(same_industry=True).count()  # Filter by logged-in user


    context = {
        'vendor_count': vendor_count,
        'highest_department': highest_department,
        'highest_count': highest_count,
        'highest_state_value': highest_state_value,
        'highest_state_count': highest_state_count,
        'true_same_industry_count': true_same_industry_count,
        'state_data': state_data,
        'enable_option':enable_option,
        'department_data': department_data,
    }
   
    return render(request, 'vendor/vendor.html',context)

def forms(request, username):
     user = User.objects.get(username=username)
     
     departments = DepartmentType.objects.filter(creator=user)
     if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        company_name = request.POST.get('company_name')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        product_name = request.POST.get('product_name')
        department = request.POST.get('department')
        website_name = request.POST.get('website_name')
        description = request.POST.get('description')
        same_industry = bool(request.POST.get('same_industry'))
        specific_appointment = request.POST.get('appointment')
        user = user

        Vendor.objects.create(
            first_name=first_name,
            company_name=company_name,
            state=state,
            phone=phone,
            email=email,
            product_name=product_name,
            department=department,
            website_name=website_name,
            description=description,
            same_industry=same_industry,
            specific_appointment=specific_appointment,
            user=user
        )
        # Send an email notification to the DepartmentType's emailaddress
        try:
            department_type = DepartmentType.objects.get(dname=department)  # Retrieve the DepartmentType
            from_email = 'leadlogix.communications@gmail.com'
            
            subject1 = 'Thank You'
            message1 = f'Dear {first_name},\n\nThank you for reaching out to us with your inquiry regarding potential collaboration. We appreciate your interest and the opportunity to explore potential partnerships.\n\nOur team will be reviewing the details you provided, and get back to you as soon as possible with the relevant information and next steps.\n\nWe value the prospect of working with you and look forward to the possibility of a successful collaboration. Thank you for considering us.\nRegards,\nTeam Operations'

            
            send_mail(subject1, message1, from_email, [email], fail_silently=False)

            subject2 = 'New Vendor Request'
            message2 = f'Hello,\n\nA new enquiry has been submitted with the following details:\n\nFirst Name: {first_name}\nCompany Name: {company_name}\nState: {state}\nPhone: {phone}\nEmail: {email}\nProduct Name: {product_name}\nDepartment: {department}\nWebsite Name: {website_name}\nDescription: {description}\nSupplied to Same Industry: {same_industry}\nSpecific Appointment: {specific_appointment}'
            
            send_mail(subject2, message2, from_email, [department_type.emailaddress], fail_silently=False)
        except DepartmentType.DoesNotExist:
            pass  # Handle the case where the DepartmentType does not exist

        response_data = {'success': True}
        return JsonResponse(response_data)

     
     return render(request,'vendor/form.html',{'departments': departments})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def reports(request):
    user = request.user
    enable_option = user.has_perm('vendor.can_view_vendor')  # Assuming the user is logged in
    vendors = Vendor.objects.filter(user=user)
     # Handle department filter
    department_filter = request.GET.get('department_filter')

    if department_filter:
        vendors = vendors.filter(department=department_filter)
        state_filter = request.GET.get('state')
        department_filter = request.GET.get('department_filter')
        # Filter data based on the filters
        vendors = Vendor.objects.filter(user=request.user)
        if state_filter:
            vendors = vendors.filter(state=state_filter)
        if department_filter:
            vendors = vendors.filter(department=department_filter)


    paginator = Paginator(vendors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get distinct department values for the filter dropdown
    distinct_departments = Vendor.objects.values_list('department', flat=True).distinct()
    department_options = DepartmentType.objects.all()
    context = {
        'vendors': vendors,
        'page_obj': page_obj,
        'distinct_departments': distinct_departments,
        'selected_department': department_filter,
        'enable_option': enable_option,
        'department_options': department_options,
    }
    return render(request, "vendor/reports.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def fetch(request):
    # Get filter parameters from request
    state_filter = request.GET.get('state')
    department_filter = request.GET.get('department')

    # Filter data based on the filters
    vendors = Vendor.objects.filter(user=request.user)
    if state_filter:
        vendors = vendors.filter(state=state_filter)
    if department_filter:
        vendors = vendors.filter(department=department_filter)

    # Define the data dictionary with default values
    data = {
        'Name': [],
        'Company Name': [],
        'Location': [],
        'Phone No': [],
        'Email': [],
        'Product Name': [],
        'Department': [],
    }

    # Populate the data dictionary if vendors exist
    if vendors:
        data = {
            'Name': [vendor.first_name for vendor in vendors],
            'Company Name': [vendor.company_name for vendor in vendors],
            'Location': [vendor.state for vendor in vendors],
            'Phone No': [vendor.phone for vendor in vendors],
            'Email': [vendor.email for vendor in vendors],
            'Product Name': [vendor.product_name for vendor in vendors],
            'Department': [vendor.department for vendor in vendors],
            
        }

    # Check if there is no data
    if not data['Name']:
        # Return an empty Excel file
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="empty_data.xlsx"'
        return response

    df = pd.DataFrame(data)

    # Create an Excel response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="filtered_data.xlsx"'
    df.to_excel(response, index=False)

    return response 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def department(request):
    user = request.user
    enable_option = user.has_perm('vendor.can_view_vendor')
    departments = DepartmentType.objects.filter(creator=request.user)  # Filter products by the logged-in user
    form = DepartmentForm()

    if request.method == 'POST': 
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.creator = request.user  # Set the creator to the logged-in user
            department.save()
            return redirect('department')

    return render(request, 'vendor/department.html', {'departments': departments, 'form': form,'enable_option': enable_option})

@csrf_exempt  # Add this decorator to disable CSRF protection for this view (for demonstration purposes)
def remove_dname(request):
    if request.method == 'POST':
        dname = request.POST.get('dname')
        emailaddress = request.POST.get('emailaddress')
        try:
            # Assuming 'dname' and 'emailaddress' together are unique identifiers
            department = DepartmentType.objects.get(dname=dname, emailaddress=emailaddress)
            department.delete()
            return JsonResponse({'message': 'Department deleted successfully'})
        except DepartmentType.DoesNotExist:
            return JsonResponse({'message': 'Department not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

