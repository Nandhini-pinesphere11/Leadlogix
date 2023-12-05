from django.shortcuts import render,redirect,get_object_or_404
from .forms import ContactForm, DateFilterForm,EmployeeForm,ComposeMessageForm
from .models import Contact,Notification,BrandMailer,EventType,BrandAttachment,ComposeAttachment,ComposeMessage
import mimetypes
from excustomer.models import ExCustomer
import openpyxl
from django.http import HttpResponse

from django.db.models import Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from .forms import ProductForm
from datetime import datetime

from .models import Employee
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from .models import ProductType, CustomizedEmail, Attachment
from django.core.mail import send_mail, EmailMessage

import requests

def send_whatsapp_message(phno):
    # Assuming you have obtained the API credentials
    api_key = 'EAAEofZBKJ4F0BO0vW1oK9kC1iwAibPZCSlsJAfi2c8QeBCo18O5HEaVbwMqJHM8ZACOMdlTYchAGbggZBaREbB9B7rIZCcZCvZA2B5OL7bMKSCtEqNq4PACgqtsN0rP0xZAR4dbfsFtU17XAjHmCs2ZARTOFNZBrq0sWAyHKZAq3eEQTH4QYCF3UesRRAIyfbmOyAqP'
    access_token = 'EAAEofZBKJ4F0BO0vW1oK9kC1iwAibPZCSlsJAfi2c8QeBCo18O5HEaVbwMqJHM8ZACOMdlTYchAGbggZBaREbB9B7rIZCcZCvZA2B5OL7bMKSCtEqNq4PACgqtsN0rP0xZAR4dbfsFtU17XAjHmCs2ZARTOFNZBrq0sWAyHKZAq3eEQTH4QYCF3UesRRAIyfbmOyAqP'
    
    # URL for sending WhatsApp messages
    url = 'https://graph.facebook.com/v17.0/135544389650536/messages'
    
    # Phone number to send the message to (extract it from the form submission)
    phone_number = phno
    
    # Prepare the request headers with API credentials
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'Authorization': f'Bearer {access_token}'
    }
    
    # Prepare the request payload with message details
    payload = {
        'to': f'whatsapp:{phone_number}',
        'type': 'template',
        'messaging_product': 'whatsapp',
        'template': {
            'name': 'hello_world',
            'language': {
                'code': 'en_US'
            }
        }
    }
    
    # Make the API request to send the WhatsApp message
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the message was sent successfully
    if response.status_code == 200:
        print(f'Message sent successfully to {phone_number}!')
        return HttpResponse('Message sent successfully!')
    else:
        print(f'Error sending message to {phone_number}: {response.text}')
        return HttpResponse(f'Error sending message: {response.text}', status=response.status_code)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def fetch_data(request):
    user_group = request.user.groups.first()
    if user_group:
        contacts = Contact.objects.filter(company_name=user_group.name)
    else:
        contacts = Contact.objects.none()

    state_filter = request.GET.get('state')  # Get the state filter from the query string
    date_filter_choice = request.GET.get('date_filter')
    selected_data = request.GET.get('selected_data')
    product_data = request.GET.get('product_data')
    selected_date = request.GET.get('selected_date')
    engaged_by = request.GET.get('engaged_by')


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Data_Export.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Data Export'

    if state_filter:
        data = contacts.filter(state=state_filter).all()
    elif selected_data:
        data = contacts.filter(customer_confidence=selected_data).all()
    elif product_data:
        data = contacts.filter(interested_products__contains=product_data).all()
    elif selected_date:
        date_formats = ['%d %m %Y', '%b. %d, %Y', '%B %d, %Y']
        parsed_date = None        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(selected_date, date_format).date()
                break
            except ValueError:
                continue
        if parsed_date:
            print("Selected Date:", parsed_date)
            data = contacts.filter(date_of_enquiry__date=parsed_date)
    elif engaged_by:
        try:
            employee = Employee.objects.get(employee_name=engaged_by)
            data = contacts.filter(engaged_by=employee).all()
        except Employee.DoesNotExist:
            # Handle the case where the employee with the provided name does not exist
            data = []
    elif date_filter_choice == 'last_three_days':
        start_date = timezone.now() - timedelta(days=3)
        data = contacts.filter(date_of_enquiry__gte=start_date).all()
    elif date_filter_choice == 'yesterday':
        end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=1)
        data = contacts.filter(date_of_enquiry__range=(start_date, end_date)).all()
    elif date_filter_choice == 'today':
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        data = contacts.filter(date_of_enquiry__range=(start_date, end_date)).all()
    else:
        data = contacts.all()    

    worksheet.append(['name', 'Date_of_enquiry', 'phone_number', 'Email', 'Engaged By', 'State', 'Customer Confidence', 'Products'])  # Adding headers

    for contact in data:
        engaged_by_name = ''
        if contact.engaged_by:  # Check if engaged_by exists
            engaged_by_name = contact.engaged_by.employee_name  # If exists, retrieve the employee_name
        worksheet.append([
            contact.first_name,
            contact.date_of_enquiry.replace(tzinfo=None),  # Remove timezone info
            contact.phone,
            contact.email,
            engaged_by_name,  # Use the retrieved employee_name or empty string if engaged_by is None
            contact.state,
            contact.customer_confidence,
            contact.interested_products,
        ])

    workbook.save(response)
    return response


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def index1(request):
    form = ContactForm()
    # Get the logged-in user's group or company
    user_group = request.user.groups.first()  # Assuming you have only one group per user
    

    if user_group:
        # Filter contacts based on the user's group or company
        contacts = Contact.objects.filter(company_name=user_group.name)
        contact_count = Contact.objects.filter(company_name=user_group.name).count()
        ex_customer_count = ExCustomer.objects.filter(company_name=user_group.name).count()
    else:
        # Handle the case where the user doesn't belong to any group
        contacts = Contact.objects.none()

    contact_count = contacts.count()

    # Get the current date
    current_date = timezone.localtime(timezone.now()).date()

   # Get the count of contacts enquired today for the user's company
    contacts_today = Contact.objects.filter(
    date_of_enquiry__date=current_date,
    company_name=user_group.name  # Assuming you have only one group per user
    )
    contact_count_today = contacts_today.count()

    events = EventType.objects.all()
    events_count = events.count()


    # Count the occurrences of each state and order them by count in descending order
    # Calculate engagement counts for the user's company
    engage_counts = contacts.values('engaged_by__employee_name').annotate(count=Count('engaged_by')).order_by('-count')

    # Get the state with the highest count for the user's company
    highest_engage = engage_counts.first()
    highest_engage_value = highest_engage['engaged_by__employee_name'] if highest_engage else None
    highest_engage_count = highest_engage['count'] if highest_engage else 0
    # Count the occurrences of each state for the user's company and order them by count in descending order
    state_counts = contacts.values('state').annotate(count=Count('state')).order_by('-count')

    # Get the state with the highest count for the user's company
    highest_state = state_counts.first()
    highest_state_value = highest_state['state'] if highest_state else None
    highest_state_count = highest_state['count'] if highest_state else 0

    # Calculate state data for the user's company
    state_data = contacts.values('state').annotate(contact_count=Count('state')).order_by('-contact_count')

    # Calculate the total count of contacts for the user's company
    total_contacts = contacts.count()

    # Calculate the progress_percentage for each state based on its count for the user's company
    for state in state_data:
        state['progress_percentage'] = (state['contact_count'] / total_contacts) * 100 if total_contacts > 0 else 0

    # Initialize a list to store product data
    product_data = []

    # Loop through contacts to extract and count unique products
    for contact in contacts:
        # Split the interested_products field by commas and strip whitespace
        products = [p.strip() for p in contact.interested_products.split(',')]
        # Update the count for each product
        for product in products:
            # Check if the product is already in product_data
            if product:
                found = False
                for entry in product_data:
                    if entry['name'] == product:
                        entry['count'] += 1
                        found = True
                        break
                if not found:
                    product_data.append({'name': product, 'count': 1})

    # Calculate the total number of products
    total_products = sum(entry['count'] for entry in product_data)

    # Calculate the product_count_percentage for each product
    for entry in product_data:
        entry['product_count_percentage'] = (entry['count'] / total_products) * 100 if total_products > 0 else 0
        # Now unique_product_counts contains the count for each unique product


    context = {
        'contacts': contacts,
        'contact_count': contact_count,
        'ex_customer_count':ex_customer_count,
        'contact_count_today': contact_count_today,
        'highest_engage_count': highest_engage_count,
        'highest_engage_value': highest_engage_value,
        'highest_state_value': highest_state_value,
        'highest_state_count': highest_state_count,
        'state_data': state_data,
        'product_data': product_data,
        'form': form,
        'events_count': events_count,
    }
    return render(request, 'index1.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageforms(request):
    products=ProductType.objects.all()
    # Get the logged-in user's group or company
    user_group = request.user.groups.first()  # Assuming you have only one group per user

    # Filter contacts based on the user's group or company
    if user_group:
        contacts = Contact.objects.filter(company_name=user_group.name).order_by('-date_of_enquiry')
    else:
        contacts = Contact.objects.none()  # Handle the case where the user doesn't belong to any group

    selected_data = request.GET.get('selected_data')
    if selected_data:
        contacts = contacts.filter(customer_confidence=selected_data)

    engage_filter = request.GET.get('engaged_by')
    if engage_filter:
        contacts = contacts.filter(engaged_by__employee_name=engage_filter)

    state_filter = request.GET.get('state')
    if state_filter:
        contacts = contacts.filter(state=state_filter)

    product_data = request.GET.get('product_data')
    if product_data:
        contacts = contacts.filter(interested_products__contains=product_data)

    selected_date = request.GET.get('selected_date')  # Retrieve selected date from query parameters

    if selected_date:
        date_formats = ['%d %m %Y', '%b. %d, %Y', '%B %d, %Y']
        parsed_date = None
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(selected_date, date_format).date()
                break
            except ValueError:
                continue
        
        if parsed_date:
            print("Selected Date:", parsed_date)
            contacts = contacts.filter(date_of_enquiry__date=parsed_date)

    form = DateFilterForm(request.GET)  # Create the form instance

    if form.is_valid():  # Check if the form is valid
        date_filter_choice = form.cleaned_data.get('date_filter')  # Access cleaned_data
        if date_filter_choice:
            if date_filter_choice == 'last_three_days':
                start_date = timezone.now() - timedelta(days=3)
                contacts = contacts.filter(date_of_enquiry__gte=start_date)
            elif date_filter_choice == 'yesterday':
                end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                start_date = end_date - timedelta(days=1)
                contacts = contacts.filter(date_of_enquiry__range=(start_date, end_date))
            elif date_filter_choice == 'today':  # Add this block for today's enquiries
                start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
                contacts = contacts.filter(date_of_enquiry__range=(start_date, end_date))  
      
    contacts = contacts.order_by('-date_of_enquiry')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    existing_message = ComposeMessage.objects.first()
    compose_form = ComposeMessageForm(instance=existing_message)
    context = {
        'page_obj': page_obj,
        'state_filter': state_filter,
        'form': form,
        'selected_data': selected_data,
        'date_filter_choice': date_filter_choice,
        'product_data': product_data,
        'selected_date': selected_date,
        'engaged_by': engage_filter,
        'compose_form': compose_form,
        'products':products,
    }
    return render(request, 'manageforms.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_customer_confidence_data(request):
    # Get the logged-in user's group or company
    user_group = request.user.groups.first()  # Assuming you have only one group per user

    if user_group:
        # Query your database to get the count of each confidence level for the user's company
        confidence_data = Contact.objects.filter(company_name=user_group.name, customer_confidence__isnull=False).values('customer_confidence').annotate(count=Count('customer_confidence'))
        total_count = Contact.objects.filter(company_name=user_group.name, customer_confidence__isnull=False).count()
    else:
        confidence_data = []
        total_count = 0

    # Prepare data for the chart
    labels = []
    values = []

    for item in confidence_data:
        confidence_level = item['customer_confidence']
        count = item['count']
        labels.append(confidence_level)
        values.append(count)

    data = {
        'labels': labels,
        'values': values,
        'total_count': total_count,
    }

    return JsonResponse(data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_contact_count(request):
    user_group = request.user.groups.first()
    if user_group:
        contact_count_data = Contact.objects.filter(company_name=user_group.name).annotate(date=TruncDate('date_of_enquiry')).values('date').annotate(count=Count('id')).order_by('date')
    else:
        contact_count_data = []

    return JsonResponse(list(contact_count_data), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_engage_data(request):
    user_group = request.user.groups.first()
    if user_group:
        engage_data = Contact.objects.filter(company_name=user_group.name, engaged_by__isnull=False).values('engaged_by__employee_name').annotate(count=Count('id')).order_by('engaged_by')
    else:
        engage_data = []

    data_list = [{'engaged_by': item['engaged_by__employee_name'], 'count': item['count']} for item in engage_data]

    return JsonResponse(data_list, safe=False)



def products_add(request):
    products = ProductType.objects.filter(creator=request.user)  # Filter products by the logged-in user

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user  # Set the creator to the logged-in user
            product.save()
            return redirect('product_list')

    form = ProductForm()  # Move this line outside of the if request.method block

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'add_products.html', context)


from django.http import JsonResponse
from django.contrib import messages

def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = ProductType.objects.get(id=product_id)
            product.delete()
            messages.success(request, f'Product {product.product_name} has been deleted.')
            return JsonResponse({'success': True})
        except ProductType.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def employee_list(request):
    employees = Employee.objects.filter(creator=request.user)  # Filter employees by the logged-in user
    form = EmployeeForm()

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.creator = request.user  # Set the creator to the logged-in user
            employee.save()
            return redirect('employee_list')

    return render(request, 'employee.html', {'employees': employees, 'form': form})

def delete_employee(request, emp_id):
    if request.method == 'POST':
        try:
            emp = Employee.objects.get(id=emp_id)
            emp.delete()
            messages.success(request, f'Employee {emp.employee_name} has been deleted.')
            return JsonResponse({'success': True})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Employee not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def product_lists(request):
    success_message = None  # Initialize a variable to store the success message

    if request.method == 'POST':
        product_name_id = request.POST.get('product_name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        attached_files = request.FILES.getlist('new_attachments')

        product_type = ProductType.objects.get(pk=product_name_id)

        # Check if a CustomizedEmail object already exists for the product type
        customized_email = CustomizedEmail.objects.filter(product=product_type).first()

        if customized_email:
            # If it exists, update the existing CustomizedEmail
            customized_email.subject = subject
            customized_email.message = message
            customized_email.save()
        else:
            # If it doesn't exist, create a new CustomizedEmail instance
            customized_email = CustomizedEmail(
                product=product_type,
                subject=subject,
                message=message,
            )
            customized_email.save()

        # Handle attached files
        for attached_file in attached_files:
            attachment = Attachment(file=attached_file)
            attachment.save()
            customized_email.attached_files.add(attachment)

        # Set the success_message variable
        success_message = "Customized email saved successfully!"

    # Fetch all product types created by the authenticated user
    product_types = ProductType.objects.filter(creator=request.user)
    customizeemails = CustomizedEmail.objects.filter(product__in=product_types)

    context = {
        'product_types': product_types,
        'customizeemails': customizeemails,
        'success_message': success_message,  # Pass the success message to the template
    }

    return render(request, 'customize_email.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def delete_attachments(request):

    if request.method == 'POST':

        attachment_id = request.POST.get('attachment_id')       

        try:

            attachment = Attachment.objects.get(id=attachment_id)

            attachment.delete()

            return JsonResponse({'success': True})

        except Attachment.DoesNotExist:

            return JsonResponse({'success': False, 'error': 'Attachment not found'})

 

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_employee_counts(request):
    # Get unique employee categories and their counts
    employee_data = Contact.objects.values('employee_count').annotate(count=Count('employee_count'))
    
    # Extract labels and values
    labels = [item['employee_count'] for item in employee_data]
    values = [item['count'] for item in employee_data]
    
    data = {
        'labels': labels,
        'values': values,
    }
    
    return JsonResponse(data)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_unread_notifications(request):
    notifications = Notification.objects.filter(read=False)
    notification_data = [
        {'message': notification.message, 'created_at': notification.created_at}
        for notification in notifications
    ]
    return JsonResponse({'notifications': notification_data})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def clear_notifications(request):
    if request.method == 'POST':
        # Clear all notifications (you can customize this based on your implementation)
        Notification.objects.all().delete()
        return JsonResponse({'message': 'Notifications cleared successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})
    



def mainform(request):    
    # Fetch the choices for customer_confidence from your model

    customer_confidence_choices = Contact.CUSTOMER_CONFIDENCE_CHOICES

    state_choices = Contact.STATE_CHOICES

    country_code_choices = Contact.COUNTRY_CODE_CHOICES 

    # Fetch the choices for engaged_by from your User model or any other source

    engaged_by_choices = Employee.objects.filter(creator_id=2)  # Replace this with your user query

    first_name = request.GET.get('first_name')
    state = request.GET.get('state')

    context = {
        'first_name': first_name,
        'state': state,
        
        'customer_confidence_choices': customer_confidence_choices,

        'engaged_by_choices': engaged_by_choices,

        'state_choices': state_choices,

        'country_code_choices': country_code_choices,

    }

    if request.method == 'POST':

        # Handle the form submission here

        first_name = request.POST['first_name']

        state = request.POST['state']

        phone_country_code = request.POST.get('phone_country_code', '+91')

        phone = request.POST['phone']

        email = request.POST['email']

        customer_confidence = request.POST.get('customer_confidence', None)

        engaged_by_id = request.POST.get('engaged_by', None)

        if engaged_by_id is not None:
            engaged_by = Employee.objects.get(id=engaged_by_id)
        else:
            engaged_by = None
        # Fetch the selected products from the request

        selected_products = request.POST.getlist('selected_products') 
        print(selected_products)

        # Join the selected products into a single string

        selected_products_str = ', '.join(selected_products)

        # Create and save a Customer object

        customer = Contact(

            first_name=first_name,

            state=state,

            phone_country_code=phone_country_code,

            phone=phone,

            email=email,

            interested_products=selected_products_str,  # Save as a single string

            customer_confidence=customer_confidence,

            engaged_by=engaged_by,

            company_name = "Strings",

        )

        customer.save()
        contact_id = customer.pk
        contacts = Contact.objects.get(pk=contact_id)
        products = [p.strip() for p in contacts.interested_products.split(',')]
        
        context = {
            'first_name': first_name,
        }
        phno = phone_country_code + phone
        send_whatsapp_message(phno)
        
        # Prepare attachments for the BrandMailer email
        brandmailer = BrandMailer.objects.get()
        subject1 = brandmailer.subject
        message1 = brandmailer.message
        from_email = 'leadlogix.communications@gmail.com'  # Change this to your email address
        recipient_list = [email]
        brandmailer_attachments = brandmailer.attachments.all()

        # Send individual product emails
        for product in products:
            print(product)
            try:
                product_email = ProductType.objects.get(product_name=product)
                print(product_email)
                customized_email = CustomizedEmail.objects.get(product=product_email)
                print(customized_email)

                subject = customized_email.subject
                message = customized_email.message
                attached_files = customized_email.attached_files.all()

                # Prepare and send the email
                email = EmailMessage(
                    subject,
                    message,
                    from_email,
                    recipient_list
                )

                for attachment in attached_files:
                    email.attach_file(attachment.file.path)

                email.send()

            except ProductType.DoesNotExist:
                print("Product does not exist")

        # Send the BrandMailer email with all attachments
        brandmailer_email = EmailMessage(
            subject1,
            message1,
            from_email,
            recipient_list
        )
        
        for attachment in brandmailer_attachments:
            brandmailer_email.attach_file(attachment.file.path)

        brandmailer_email.send()

        # Redirect to a thank you page or any other desired page
        return redirect('mainform') 

    return render(request, 'Form/main_form.html', context)


 

def get_product(request):

    products = ProductType.objects.filter(creator_id=2)

    product_list = [product.product_name for product in products]

    return JsonResponse(product_list, safe=False)


def brand(request):
    saved_attachments = BrandAttachment.objects.all()  # Fetch saved attachments data

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        # Create a new BrandMailer instance or get an existing one
        try:
            brand_mailer = BrandMailer.objects.get()
        except BrandMailer.DoesNotExist:
            brand_mailer = BrandMailer()

        brand_mailer.subject = subject
        brand_mailer.message = message
        brand_mailer.save()

        # Handle file attachments
        attachments = request.FILES.getlist('attachments')
        for attachment in attachments:
            attachment_instance = BrandAttachment(file=attachment)
            attachment_instance.save()
            brand_mailer.attachments.add(attachment_instance)

        return redirect('brand')
    else:
        try:
            brand_mailer = BrandMailer.objects.get()
            initial_data = {'subject': brand_mailer.subject, 'message': brand_mailer.message}
        except BrandMailer.DoesNotExist:
            initial_data = {'subject': '', 'message': ''}

        return render(request, 'brand.html', {'initial_data': initial_data,'saved_attachments':saved_attachments})

def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(BrandAttachment, id=attachment_id)

    # Delete the attachment from the database
    attachment.delete()

    # Redirect to the same page or a different URL
    return redirect('brand')

def get_existing_employee(request):
    user_group = request.user.groups.first()
    if user_group:
        contact_count = Contact.objects.filter(company_name=user_group.name).count()
        ex_customer_count = ExCustomer.objects.filter(company_name=user_group.name).count()
    else:
        contact_count = 0
        ex_customer_count = 0

    data = [
        {'engaged_by': 'New Customer', 'count': contact_count},
        {'engaged_by': 'Existing Customer', 'count': ex_customer_count}
    ]
    return JsonResponse(data, safe=False)


def compose_message(request):
    existing_message = ComposeMessage.objects.first()
    form = ComposeMessageForm(instance=existing_message)

    if request.method == 'POST':
        selected_emails = request.POST.get('selectedEmails', '').split(',')

        # Check if there are any selected emails
        if not selected_emails or all(email.strip() == '' or email.strip().lower() == 'none' for email in selected_emails):
            messages.error(request, 'Please provide valid email addresses.')
            return redirect('manageforms')

        form = ComposeMessageForm(request.POST, request.FILES, instance=existing_message)

        if form.is_valid():
            new_message = form.save(commit=False)

            # Clear existing attachments before adding new ones
            new_message.attachments.clear()

            # Handle attachments obtained through AJAX (related to the selected product)
            attachments_from_ajax = form.cleaned_data['attachments'].split(',')
            existing_attachments = ComposeAttachment.objects.filter(file__in=attachments_from_ajax)
            new_attachments = []

            for attachment in attachments_from_ajax:
                attachment_obj, created = existing_attachments.get_or_create(file=attachment)
                new_message.attachments.add(attachment_obj)
                new_attachments.append(attachment_obj)

            # Handle manual attachments (selected through file input)
            for file in request.FILES.getlist('attachments'):
                attachment_obj, created = ComposeAttachment.objects.get_or_create(file=file)
                new_message.attachments.add(attachment_obj)
                new_attachments.append(attachment_obj)

            new_message.save()  # Save the message again after adding attachments

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email = EmailMessage(subject, message, 'leadlogix.communications@gmail.com', selected_emails)

            for attachment in new_attachments:
                if attachment.file and attachment.file.file:
                    file_obj = attachment.file.file
                    content_type = getattr(file_obj, 'content_type', None)
                    if not content_type:
                        content_type, _ = mimetypes.guess_type(attachment.file.name)
                    email.attach(attachment.file.name, file_obj.read(), content_type)

            email.send()
            messages.success(request, 'Email sent successfully!')
            return redirect('manageforms')
        else:
            # Print form errors
            print(form.errors)
            messages.error(request, 'Form submission failed. Please check the form for errors.')

    return render(request, 'manageforms.html', {'form': form})




# views.py

def get_customized_email(request):
    product_id = request.GET.get('product_id')
    try:
        customized_email = CustomizedEmail.objects.get(product_id=product_id)
        data = {
            'subject': customized_email.subject,
            'message': customized_email.message,
            'attachments': [str(attachment) for attachment in customized_email.attached_files.all()],
        }
        return JsonResponse(data)
    except CustomizedEmail.DoesNotExist:
        return JsonResponse({'error': 'CustomizedEmail not found for the selected product'})