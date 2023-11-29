from django import forms
from .models import ExCustomer  # Import your model
from app1.models import ProductType  # Import your model

class ExCustomerForm(forms.ModelForm):
    class Meta:
        model = ExCustomer
        fields = '__all__'  # You can specify fields explicitly if needed

    # Update interested_products field to use ModelMultipleChoiceField
    interested_products = forms.ModelMultipleChoiceField(
        queryset=ProductType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
