from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import appeal_master


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
        fields = ['case_number', 'rep_id', 'fi_id', 'prrb_contact_id', 'status_id', 'appeal_name', 'structure', 'request_date']
