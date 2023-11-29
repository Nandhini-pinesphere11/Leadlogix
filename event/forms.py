from django import forms
from .models import EventType
from datetime import timedelta

class EventForm(forms.ModelForm):
    venue = forms.ChoiceField(choices=[('', 'Select a Venue')] + EventType.STATE_CHOICES)
    class Meta:
        model = EventType
        fields = ['ename', 'venue', 'start_date', 'end_date']
        labels = {
            'ename': 'Enter an Event Name',
            'start_date': 'Enter a Start Date',
            'end_date': 'Enter an End Date',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DateFilterForms(forms.Form):
    date_filter = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Date Filter'
    )

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id', None)

        super(DateFilterForms, self).__init__(*args, **kwargs)

        if event_id:
            try:
                event = EventType.objects.get(id=event_id)
                start_date = event.start_date
                end_date = event.end_date

                date_choices = []
                current_date = start_date

                while current_date <= end_date:
                    date_choices.append((current_date.strftime('%Y-%m-%d'), current_date.strftime('%Y-%m-%d')))
                    current_date += timedelta(days=1)

                self.fields['date_filter'].choices = [('all', 'Overall Report')] + date_choices

            except EventType.DoesNotExist:
                pass