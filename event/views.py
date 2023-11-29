from django.shortcuts import render,redirect,get_object_or_404
from .models import EventType
from .forms import EventForm
import openpyxl
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from app1.models import Contact,ProductType,Employee,CustomizedEmail,BrandMailer
from django.template.loader import render_to_string
from django.contrib import messages

from django.contrib.auth.models import User
  # Import your Customer model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.utils import timezone
  # Import your Event model here
from event.forms import DateFilterForms  # Import your DateFilterForm here
  # Import your Event model here
from app1.forms import ContactForm,ComposeMessageForm # Import your ContactForm here
from app1.models import ComposeMessage,ComposeAttachment
import mimetypes
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.mail import send_mail, EmailMessage
from dateutil import parser


# Create your views here. 
def Create_event(request):
    events = EventType.objects.filter(creator=request.user)  # Filter products by the logged-in user

    form = EventForm() 

    if request.method == 'POST': 
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user  # Set the creator to the logged-in user
            event.save()
            return redirect('Create_event')
    return render(request, 'event/event.html',{'events': events, 'form': form}) 

@csrf_exempt
def remove_ename(request):
    if request.method == 'POST':
        ename = request.POST.get('ename')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        try:
            # Find the event to delete based on ename, startdate, and enddate
            event = EventType.objects.get(ename=ename)
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'})
        except EventType.DoesNotExist:
            return JsonResponse({'message': 'Event not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def event_dashboard(request,username, event_id):
    form = ContactForm()
    # Retrieve the event using the event_id
    event = get_object_or_404(EventType, id=event_id)  # Replace 'EventType' with your event model

    # Filter contacts based on the selected event
    contacts = Contact.objects.filter(event=event)  # Replace 'Contact' with your report model

    contact_count = contacts.count()

    # Get the current date
    current_date = timezone.localtime(timezone.now()).date()

    # Get the count of contacts enquired today for the selected event
    contacts_today = Contact.objects.filter(
        date_of_enquiry__date=current_date,
        event=event
    )
    contact_count_today = contacts_today.count()

    # Count the occurrences of each state and order them by count in descending order
    # Calculate engagement counts for the selected event
    engage_counts = contacts.values('customer_confidence').annotate(count=Count('customer_confidence')).order_by('-count')

    # Get the state with the highest count for the selected event
    highest_engage = engage_counts.first()
    highest_engage_value = highest_engage['customer_confidence'] if highest_engage else None
    highest_engage_count = highest_engage['count'] if highest_engage else 0

    # Count the occurrences of each state for the selected event and order them by count in descending order
    state_counts = contacts.values('state').annotate(count=Count('state')).order_by('-count')

    # Get the state with the highest count for the selected event
    highest_state = state_counts.first()
    highest_state_value = highest_state['state'] if highest_state else None
    highest_state_count = highest_state['count'] if highest_state else 0

    # Calculate state data for the selected event
    state_data = contacts.values('state').annotate(contact_count=Count('state')).order_by('-contact_count')

    # Calculate the total count of contacts for the selected event
    total_contacts = contacts.count()

    # Calculate the progress_percentage for each state based on its count for the selected event
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
    context = {
        'event': event,
        'contacts': contacts,
        'contact_count': contact_count,
        'contact_count_today': contact_count_today,
        'highest_engage_count': highest_engage_count,
        'highest_engage_value': highest_engage_value,
        'highest_state_value': highest_state_value,
        'highest_state_count': highest_state_count,
        'state_data': state_data,
        'total_contacts': total_contacts,
        'product_data': product_data,
        'form': form,
        'username': request.user.username,
    }
    return render(request, 'event/event_base.html', context)


def event_reports(request, username, event_id):
    # Retrieve the event using the event_id
    event = get_object_or_404(EventType, id=event_id)  # Replace 'EventType' with your event model

    # Filter the reports associated with the event
    reports = Contact.objects.filter(event=event)  # Replace 'Contact' with your report model

    selected_data = request.GET.get('selected_data')
    if selected_data:
        reports = reports.filter(customer_confidence=selected_data)

    engage_filter = request.GET.get('engaged_by')
    if engage_filter:
        reports = reports.filter(engaged_by__employee_name=engage_filter)

    state_filter = request.GET.get('state')
    if state_filter:
        reports = reports.filter(state=state_filter)

    product_data = request.GET.get('product_data')
    if product_data:
        reports = reports.filter(interested_products__contains=product_data)

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
            reports = reports.filter(date_of_enquiry__date=parsed_date)

    form = DateFilterForms(request.GET, event_id=event_id)  # Create the form instance

    if form.is_valid():  # Check if the form is valid
        date_filter_choice = form.cleaned_data.get('date_filter')  # Access cleaned_data

        if date_filter_choice and date_filter_choice != 'all':
            selected_date = datetime.strptime(date_filter_choice, '%Y-%m-%d').date()
            reports = reports.filter(date_of_enquiry__date=selected_date)

    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'event': event,
        'page_obj': page_obj,
        'state_filter': state_filter,
        'form': form,
        'selected_data': selected_data,
        'date_filter_choice': date_filter_choice,
        'product_data': product_data,
        'selected_date': selected_date,
        'engaged_by': engage_filter,
        'username': request.user.username,
    }
    return render(request, 'event/event_reports.html', context)

def fetch_datas(request,username, event_id):
    event = get_object_or_404(EventType, id=event_id)  # Replace 'EventType' with your event model
    # Filter the reports associated with the event
    reports = Contact.objects.filter(event=event)  # Replace 'Contact' with your report model

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
        data = reports.filter(state=state_filter).all()
    elif selected_data:
        data = reports.filter(customer_confidence=selected_data).all()
    elif product_data:
        data = reports.filter(interested_products__contains=product_data).all()
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
            data = reports.filter(date_of_enquiry__date=parsed_date)
    elif engaged_by:
        try:
            employee = Employee.objects.get(employee_name=engaged_by)
            data = reports.filter(engaged_by=employee).all()
        except Employee.DoesNotExist:
            # Handle the case where the employee with the provided name does not exist
            data = []
    elif date_filter_choice:
        data = reports.filter(date_of_enquiry__date=date_filter_choice).all()        
    else:
        data = reports.all()    

    worksheet.append(['name', 'Date_of_enquiry', 'phone_number', 'Email', 'Engaged By', 'State', 'Customer Confidence', 'Products'])  # Adding headers

    for contact in data:
        worksheet.append([
            contact.first_name,
            contact.date_of_enquiry.replace(tzinfo=None),  # Remove timezone info
            contact.phone,
            contact.email,
            contact.engaged_by.employee_name,
            contact.state,
            contact.customer_confidence,
            contact.interested_products,
        ])

    workbook.save(response)
    return response


def event_form(request, event_id):

    event = get_object_or_404(EventType, pk=event_id)

    user="Strings"

    # Fetch the choices for customer_confidence from your model

    customer_confidence_choices = Contact.CUSTOMER_CONFIDENCE_CHOICES

    state_choices = Contact.STATE_CHOICES

    country_code_choices = Contact.COUNTRY_CODE_CHOICES 

    # Fetch the choices for engaged_by from your User model or any other source

    engaged_by_choices = Employee.objects.filter(creator_id=2)  # Replace this with your user query 

    context = {

        'event': event,  # Assuming 'events' is a list of events you want to display

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
            company_name = user,
            event=event,  # Associate the event with the Contact

        )
        customer.save()
        contact_id = customer.pk
        contacts = Contact.objects.get(pk=contact_id)
        products = [p.strip() for p in contacts.interested_products.split(',')]
        context = {
            'first_name': first_name,
        }
        # Prepare attachments for the BrandMailer email
        brandmailer = BrandMailer.objects.get()
        subject1 = brandmailer.subject
        message1 = brandmailer.message
        from_email = 'leadlogix.communications@gmail.com'  # Change this to your email address
        recipient_list = [email]
        brandmailer_attachments = brandmailer.attachments.all()

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
                print("Product Does not exist")
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
        # Redirect to the same event_form view
        return redirect('event_form',event_id=event.id)

    return render(request, 'event/event_form.html', context)


def login_view(request):
    if request.method == 'POST':
        # Create an instance of the AuthenticationForm and pass the POST data to it
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to a success page or any desired page
                return redirect('event_dashboard')  # Replace with the name of your success page

    else:
        form = AuthenticationForm()

    # Render the login form
    return render(request, 'event/signin.html', {'form': form})

def get_products(request):

    products = ProductType.objects.filter(creator_id=2)
    product_list = [product.product_name for product in products]
    return JsonResponse(product_list, safe=False)

def get_customer_confidence_datas(request, event_id):
    # Retrieve the event using the event_id
    event = get_object_or_404(EventType, id=event_id)

    # Get the logged-in user's group or company
    user_group = request.user.groups.first()  # Assuming you have only one group per user

    if user_group:
        # Query your database to get the count of each confidence level for the user's company
        confidence_data = Contact.objects.filter(company_name=user_group.name,customer_confidence__isnull=False, event=event).values('customer_confidence').annotate(count=Count('customer_confidence'))
        total_count = Contact.objects.filter(company_name=user_group.name,customer_confidence__isnull=False, event=event).count()
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

def get_contact_counts(request, event_id):
    user_group = request.user.groups.first()
    
    if user_group:
        contact_count_data = Contact.objects.filter(event_id=event_id).annotate(date=TruncDate('date_of_enquiry')).values('date').annotate(count=Count('id')).order_by('date')
    else:
        contact_count_data = 0
    
    return JsonResponse(list(contact_count_data), safe=False)

def get_engage_datas(request, event_id):
    user_group = request.user.groups.first()

    if user_group:
        # Filter the data based on both company and event_id
        engage_data = Contact.objects.filter(company_name=user_group.name,engaged_by__isnull=False, event_id=event_id).values('engaged_by__employee_name').annotate(count=Count('id')).order_by('engaged_by')
    else:
        engage_data = []

    data_list = [{'engaged_by': item['engaged_by__employee_name'], 'count': item['count']} for item in engage_data]

    return JsonResponse(data_list, safe=False)



def event_compose_message(request):
    existing_message = ComposeMessage.objects.first()
    form = ComposeMessageForm(instance=existing_message)
 
    if request.method == 'POST':
        selected_emails = request.POST.get('selectedEmails', '').split(',')
        event_id = request.POST.get('event_id')
        event = get_object_or_404(EventType, id=event_id)
        # Check if there are any selected emails
        if not selected_emails or all(email.strip() == '' or email.strip().lower() == 'none' for email in selected_emails):
            messages.error(request, 'Please provide valid email addresses.')
            return redirect('event_reports', username=request.user.username,event_id=event_id)  # Remove event_id for now

        form = ComposeMessageForm(request.POST, request.FILES, instance=existing_message)

        # Retrieve the event object
        event_id = request.POST.get('event_id')
        event = get_object_or_404(EventType, id=event_id)

        if form.is_valid():
            # Save the form data
            new_message = form.save(commit=False)
            new_message.event = event
            new_message.save()

            # Save new attachments
            attachments = [ComposeAttachment(file=attachment) for attachment in request.FILES.getlist('attachments')]
            ComposeAttachment.objects.bulk_create(attachments)

            # Associate new attachments with the new_message
            new_message.attachments.set(attachments)

            # Continue with your email sending logic...
            # Send email to selected email ids with attachments
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'leadlogix.communications@gmail.com'
            recipient_list = request.POST.get('selectedEmails', '').split(',')

            email = EmailMessage(subject, message, from_email, recipient_list)

            # Attachments
            for attachment in attachments:
                file_obj = attachment.file.file
                content_type = getattr(file_obj, 'mimetype', None)

                if not content_type:
                    content_type, encoding = mimetypes.guess_type(attachment.file.name)

                email.attach(attachment.file.name, file_obj.read(), content_type)

            # Send the email
            email.send()
            messages.success(request, 'Email sent successfully!')
            # Redirect to event_reports with the necessary parameters
            return redirect('event_reports', username=request.user.username, event_id=event_id)

    return render(request, 'event_reports.html', {'form': form})

