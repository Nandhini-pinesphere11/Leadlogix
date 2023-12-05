from django.shortcuts import render,redirect,get_object_or_404
from .models import ExCustomer
from django.http import JsonResponse
from django.core.paginator import Paginator
# views.py
from .forms import ExCustomerForm  # Import your ExCustomerForm
from app1.forms import ComposeMessageForm
import mimetypes

from app1.models import Employee ,ProductType,ComposeAttachment,ComposeMessage # Import your Employee model
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
        'products':products,
        'product_types': ProductType.objects.all(),
}
    return render(request, 'excustomer/excustomer_reports.html', context)
    
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from app1.models import CustomizedEmail, BrandMailer

def edit_excustomer(request, pk):
    ex_customer = get_object_or_404(ExCustomer, pk=pk)

    if request.method == 'POST':
        form = ExCustomerForm(request.POST, instance=ex_customer)
        if form.is_valid():
            interested_products = request.POST.getlist('interested_products')

            form.save()
            print("Form saved successfully")

            # Fetch email subject and message from BrandMailer model
            brand_mailer = BrandMailer.objects.first()
            email_subject = brand_mailer.subject
            email_message = brand_mailer.message

            # Create an EmailMessage instance for the brand mailer
            brand_email = EmailMessage(email_subject, email_message, 'your_email@example.com', [ex_customer.email])

            # Add attachments from the BrandMailer model
            for attachment in brand_mailer.attachments.all():
                brand_email.attach(attachment.file.name, attachment.file.read(), 'application/pdf')

            try:
                brand_email.send()
                print("Brand mailer email sent successfully")

                # Send emails for selected products
                for product_id in interested_products:
                    product = ProductType.objects.get(pk=product_id)
                    product_email = CustomizedEmail.objects.get(product=product)

                    email_subject = product_email.subject
                    email_message = product_email.message

                    email = EmailMessage(email_subject, email_message, 'your_email@example.com', [ex_customer.email])

                    # Add attachments from the CustomizedEmail model
                    for attachment in product_email.attached_files.all():
                        email.attach(attachment.file.name, attachment.file.read(), 'application/pdf')

                    try:
                        email.send()
                        print(f"Email sent successfully for product: {product.product_name}")
                    except Exception as e:
                        print(f"Error sending email for product {product.product_name}: {str(e)}")

                # Add a success message for form submission
                messages.success(request, 'Form edited successfully')

            except Exception as e:
                print(f"Error sending brand mailer email: {str(e)}")

            return JsonResponse({'success': True})

        else:
            # Form is not valid, return form errors as JSON
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ExCustomerForm(instance=ex_customer)

    context = {
        'form': form,
        'product_types': ProductType.objects.all(),
    }

    return render(request, 'excustomer/excustomer_reports.html', context)



def view_excustomer(request, excustomer_id):
    excustomer = ExCustomer.objects.get(pk=excustomer_id)
    return render(request, 'excustomer/excustomer_reports.html', {'excustomer': excustomer})


def excustomer_compose_message(request):
    existing_message = ComposeMessage.objects.first()
    form = ComposeMessageForm(instance=existing_message)

    if request.method == 'POST':
        selected_emails = request.POST.get('selectedEmails', '').split(',')

        # Check if there are any selected emails
        if not selected_emails or all(email.strip() == '' or email.strip().lower() == 'none' for email in selected_emails):
            messages.error(request, 'Please provide valid email addresses.')
            return redirect('reports_excust')

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
            return redirect('reports_excust')
        else:
            # Print form errors
            print(form.errors)
            messages.error(request, 'Form submission failed. Please check the form for errors.')

    return render(request, 'excustomer_reports.html', {'form': form})




# views.py

def fetch_customized_email(request):
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