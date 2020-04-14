from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Textarea, DateField
from .models import appeal_master, critical_dates_master


class CalendarEventForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField()
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    location = forms.CharField()
    is_all_day = forms.BooleanField(required = False)


class new_appeal_master_form(ModelForm):

    class Meta:
        model = appeal_master
        fields = ['case_number', 'rep_id', 'fi_id', 'prrb_contact_id', 'status_id', 'appeal_name', 'structure']
        labels = {
            'case_number':_('Case Number:'),
            'rep_id':_('SRG Representative:'),
            'fi_id':_('Intermediary (MAC):'),
            'prrb_contact_id':_('PRRB Representative'),
            'status_id':_('Appeal Status:'),
            'appeal_name':_('Appeal Name:'),
            'structure':_('Structure:'),
        }

class acknowledge_case_form(forms.Form):
    acknowledged_date = forms.DateField()

    def clean_acknowledged_date(self):
        data = self.cleaned_data['acknowledged_date']
        return data


class add_critical_due_dates_form(ModelForm):

    class Meta:
        model = critical_dates_master
        fields = ['case_number','critical_date', 'action_id']
