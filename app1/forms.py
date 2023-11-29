from django import forms
from .models import Contact
from .models import ProductType
from .models import Employee,ComposeMessage

from .models import CustomizedEmail

class CustomizedEmailForm(forms.ModelForm):
    class Meta:
        model = CustomizedEmail
        fields = [ 'subject', 'message', 'attached_files']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['product_name'] 
        labels = {'product_name': 'Product Name'}

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name'] 
        labels = {'employee_name': 'Employee Name'}

class DateFilterForm(forms.Form):
    DATE_CHOICES = [
        ('all', 'Overall Report'),
        ('last_three_days', 'Last 3 Days'),
        ('yesterday', 'Yesterday\'s Enquiry'),
        ('today', 'Today\'s Enquiry'),
    ]

    date_filter = forms.ChoiceField(
        choices=DATE_CHOICES,
        required=False,  # Allow not selecting any option
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Date Filter',  # Set the label here
    )
class ComposeMessageForm(forms.ModelForm):
    attachments = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ComposeMessage
        fields = ['subject', 'message', 'attachments']

