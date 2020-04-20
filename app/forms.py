from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Textarea, DateField, CheckboxInput, TextInput
from .models import appeal_master, critical_dates_master, provider_master, issue_master, parent_master
from tinymce.widgets import HTMLField

class  make_dir_form(forms.Form):
    types = [
                ('INDIVIDUAL', 'Individual'),
                ('GROUP', 'Group')
            ]
    type = forms.ChoiceField(choices=types)
    parent = forms.ModelChoiceField(queryset=parent_master.objects.only('parent_id'))
    p_num = forms.CharField(max_length=7, required=False)
    issue = forms.ModelChoiceField(queryset=issue_master.objects.only('abbreviation'), required=False)
    fy = forms.IntegerField()
    c_num = forms.CharField(max_length=7)

class CalendarEventForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField()
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    location = forms.CharField()
    is_all_day = forms.BooleanField(required = False)

class add_issue(ModelForm):

    class Meta:
        model = provider_master
        fields = [
                    'provider_number',
                    'fiscal_year',
                    'npr_date',
                    'receipt_date',
                    'was_added',
                    'issue_id',
                    'audit_adjustments',
                    'charge_id',
                    'amount',
                    'sri_staff_id',
                    'active_in_appeal_field',
                    'provider_specific_note'
                ]
        labels = {
                    'provider_number':_('Provider Number:'),
                    'fiscal_year':_('Fiscal Year:'),
                    'npr_date':_('NPR Date:'),
                    'receipt_date': _('Reciept Date:'),
                    'was_added': _('Was Added:'),
                    'issue_id': _('Issue:'),
                    'audit_adjustments': _('Audit Adjustments:'),
                    'charge_id':_('Code:'),
                    'amount':_('Amount:'),
                    'sri_staff_id':_('SRG Staff:'),
                    'active_in_appeal_field':_('Active:'),
                    'provider_specific_note':_('Provider Specific Note:')
            }
        widgets = {
                'was_added': CheckboxInput(attrs={'class': 'checkbox'}),
                'active_in_appeal_field': CheckboxInput(attrs={'class': 'checkbox'}),
                'provider_specific_note': Textarea(attrs={'cols':75, 'rows':5})
            }

class new_appeal_master_form(ModelForm):

    class Meta:
        model = appeal_master
        fields = ['case_number', 'rep_id', 'fi_id', 'prrb_contact_id', 'status_id', 'appeal_name', 'structure','is_ffy']
        labels = {
            'case_number':_('Case Number:'),
            'rep_id':_('SRG Representative:'),
            'fi_id':_('Intermediary (MAC):'),
            'prrb_contact_id':_('PRRB Representative'),
            'status_id':_('Appeal Status:'),
            'appeal_name':_('Appeal Name:'),
            'structure':_('Structure:'),
            'is_ffy':_('FFY?')
        }
        widgets = {
            'is_ffy': CheckboxInput(attrs={'class': 'checkbox'}),
            'appeal_name': TextInput(attrs={'size': '75'}),
        }

class new_issue_master_form(ModelForm):
    class Meta:
        model = issue_master
        fields = ['issue_id', 'issue', 'rep_id','abbreviation', 'short_description','long_description']
        labels = {
            'issue_id':_('Issue ID:'),
            'rep_id':_('SRG Representative:'),
            'abbreviation':_('Issue abbreviation:'),
            'short_description':_('Short Description'),
            'long_description':_('Long Description')
        }

        widgets = {
            'short_description' : HTMLField(),
            'long_description' : HTMLField()
        }

class acknowledge_case_form(forms.Form):
    acknowledged_date = forms.DateField()

    def clean_acknowledged_date(self):
        data = self.cleaned_data['acknowledged_date']
        return data

class transfer_issue_form(forms.Form):

    to_case = forms.ModelChoiceField(queryset=appeal_master.objects.only('case_number'))
    to_date = forms.DateField()

    def clean_to_date(self):
        data = self.cleaned_data['to_date']
        return data

class add_critical_due_dates_form(ModelForm):

    class Meta:
        model = critical_dates_master
        fields = ['critical_date', 'action_id']
