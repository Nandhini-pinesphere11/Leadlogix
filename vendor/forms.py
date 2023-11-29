from django import forms

from .models import DepartmentType


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = DepartmentType
        fields = ['dname','emailaddress'] 
        labels = {'name': 'Enter a Department','email':'Enter a Email'}