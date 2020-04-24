from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from app.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from app.graph_helper import get_user, get_calendar_events, create_event
import dateutil.parser
from app.forms import *
from app.models import *
from django.views.generic import TemplateView, UpdateView, CreateView
import os
import random
import datetime
from datetime import datetime
from datetime import date, timedelta
from django.db.models import Avg, Sum
# Create your views here.


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # check for the user in the session
    context['user'] = request.session.get('user', {'is_authenticated':False})
    return context

def provider_name_master_view(request):
    context = initialize_context(request)
    token = get_token(request)

    all_providers = prov_name_master.objects.all().order_by('provider_number')

    context['all_providers'] = all_providers

    return render(request, 'app/provider_name_master.html', context)

class new_provider_name_view(CreateView):
    model = prov_name_master

    fields = [
        'provider_number',
        'provider_name',
        'fye',
        'city',
        'county',
        'state_id',
        'parent_id',
        'fi_number',
        'is_client'
    ]
    template_name = 'app/prov_name_master_create_form.html'
    context_object_name = 'provider'

    def form_valid(self, form):
        provider = form.save(commit=False)
        provider.save()
        return redirect('provider_name_master_url')

class provider_name_update_view(UpdateView):
    model = prov_name_master

    fields = [
        'provider_number',
        'provider_name',
        'fye',
        'city',
        'county',
        'state_id',
        'parent_id',
        'fi_number',
        'is_client'
    ]

    template_name = 'app/prov_name_master_form.html'
    pk_url_kwarg = 'provider_number'
    context_object_name = 'provider'

    def form_valid(self, form):
        provider = form.save(commit=False)
        provider.save()
        return redirect('provider_name_master_url')

class parent_update_view(UpdateView):
    # Specify the model
    model = parent_master

    #Specify the fields
    fields = [
            'parent_id',
            'parent_full_name',
            'corp_contact_first_name',
            'corp_contact_last_name',
            'corp_contact_street',
            'corp_contact_city',
            'corp_contact_state_id',
            'corp_contact_zip',
            'corp_contact_phone',
            'corp_contact_email'
        ]
    template_name = 'app/parent_master_form.html'
    pk_url_kwarg = 'parent_id'
    context_object_name = 'parent'

    def form_valid(self, form):
        parent = form.save(commit=False)
        parent.save()
        return redirect('parent_master_url')

def parent_master_view(request):
    context = initialize_context(request)
    token = get_token(request)

    all_parents = parent_master.objects.all().order_by('parent_id')

    context['all_parents'] = all_parents

    return render(request, 'app/parent_master.html', context)

def new_parent_view(request):
    context = initialize_context(request)
    token  = get_token(request)

    form = add_parent_form(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            new_parent = form.save(commit=False)
            new_parent.save()

            return redirect(r'parent_master_url')
        else:
            form = add_parent_form(request.POST)

    context['form'] = form

    return render(request, 'app/new_parent.html', context)

def issue_master_view(request):
    context = initialize_context(request)
    token = get_token(request)

    all_issues = issue_master.objects.all().order_by('issue_id')
    context['all_issues'] = all_issues

    return render(request, 'app/issue_master.html', context)

def issue_detail_view(request, pk):
    context = initialize_context(request)
    token = get_token(request)

    issue = get_object_or_404(issue_master, pk=pk)

    context['issue'] = issue

    return render(request, 'app/issue_master_detail.html', context)

class update_issue_view(UpdateView):
    # Specify the model
    model = issue_master

    #Specify the fields
    fields = [
            'issue_id',
            'old_id',
            'issue',
            'realization_weight',
            'rep_id',
            'abbreviation',
            'short_description',
            'long_description',
            'is_groupable'
        ]
    template_name = 'app/issue_master_form.html'
    pk_url_kwarg = 'issue_id'
    context_object_name = 'issue'

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        return redirect(r'issue_detail_url', issue.issue_id)

def delete_issue(request, pk):
    provider_master.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(reverse('home'))

def new_issue_master(request):
    context = initialize_context(request)
    token = get_token(request)

    form = new_issue_master_form(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            new_issue = form.save(commit=False)
            new_issue.save()

            return redirect(r'issue_master_url')

        else:
            form = new_appeal_master_form(request.POST)

    context['form'] = form

    return render(request, 'app/new_issue_master.html', context)

def home(request):
    context = initialize_context(request)
    due_next = critical_dates_master.objects.all().order_by('-critical_date')
    most_rec_cases = appeal_master.objects.all().order_by('-request_date')
    total_cases = appeal_master.objects.count()
    impact = provider_master.objects.filter(active_in_appeal_field__exact=True).aggregate(sum=Sum('amount'))
    ''' total_impact = '{:20,.2f}'.format(impact['sum'])'''

    if request.method =='POST' and 'make_dir_button' not in request.POST:
        search_case = request.POST.get('search')

        return redirect(r'appeal_detail_url', search_case)


    new_dir_form = make_dir_form(request.POST)
    if request.method == 'POST' and 'make_dir_button' in request.POST:
        if new_dir_form.is_valid():
            type = request.POST.get('type')
            parent = request.POST.get('parent')
            p_num = request.POST.get('p_num')
            issue = request.POST.get('issue')
            fy = request.POST.get('fy')
            c_num = request.POST.get('c_num')

            if type == 'INDIVIDUAL':
                # Goal: S:\3-AP\1-DOCS\INDIVIDUAL\IND~01-0001~2016~XX-XXXX
                new_path = 'S:\\3-AP\\1-DOCS\\{0}\{1}~{2}~{3}~{4}'.format(type, parent, p_num, fy, c_num)
            else:
                # Goal: S:\3-AP\1-DOCS\GROUP\IND~CN-XXXX~2016~1~SSI ERR
                issue_abb = issue_master.objects.get(pk=issue)
                new_path = 'S:\\3-AP\\1-DOCS\\{0}\{1}~{2}~{3}~{4}~{5}'.format(type, parent,fy,c_num,issue, issue_abb.abbreviation)

            try:
                os.mkdir(new_path)
                # Sucess Message
                messages.success(request, 'Directory created successfully!')
                new_dir_form = make_dir_form()
            except:
                # Directory Already Exists
                messages.error(request, 'Directory already exsists, please correct and try again.')

        else:
            new_dir_form = make_dir_form()

    context['new_dir_form'] = new_dir_form
    context['due_next'] = due_next
    context['most_rec_cases'] = most_rec_cases
    context['total_cases'] = total_cases


    return render(request, 'app/index.html', context)

def sign_in(request):
    # Get the sign in url
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)

def callback(request):
    # Get the state saved in the session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_user(token)

    # Save the token and user
    store_token(request, token)
    store_user(request, user)

    return HttpResponseRedirect(reverse('home'))

def sign_out(request):
    # Clear out the user and the token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))

def calendar(request):
    context = initialize_context(request)

    token = get_token(request)
    events = get_calendar_events(token)

    if events:
        for event in events['value']:
            event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
            event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

        context['events'] = events['value']

    return render(request, 'app/calendar.html', context)

def new_appeal(request):
    today = datetime.today()
    context = initialize_context(request)
    form = new_appeal_master_form(request.POST)
    context['form'] = form
    token = get_token(request)
    if request.method == 'POST':
        if form.is_valid():
            new_appeal_master_case = form.save(commit=False)
            new_appeal_master_case.request_date = today
            new_appeal_master_case.save()

            return render(request, 'app/index.html', context=context)
    return render(request, 'app/new_appeal_master.html', context=context)

def add_critical_due_dates(request, pk):
    context = initialize_context(request)
    token = get_token(request)
    case_information = get_object_or_404(appeal_master, pk=pk)
    case = case_information.case_number
    case_due_dates = critical_dates_master.objects.filter(case_number__exact=case).order_by('critical_date')
    due_form = add_critical_due_dates_form(request.POST)

    if request.method == 'POST' and 'dueButton' in request.POST:
        if due_form.is_valid():
            new_due_date = due_form.save(commit=False)
            new_due_date.case_number = case
            new_due_date.save()

            action = action_master.objects.get(pk=new_due_date.action_id)
            prov = provider_master.objects.filter(case_number__exact=case)
            p = prov[:1]
            for prov in p:
                fy = prov.fiscal_year

            if case_information.structure == 'INDIVIDUAL':
                for prov in p:
                    pnum = prov.provider_number
                o_sub = '{0}~{1}~FY{2}~({3})'.format(new_due_date.action_id, case, str(fy) ,pnum)
            else:
                o_sub = '{0}~{1}G~FY{2}'.format(new_due_date.action_id, case, str(fy))

            # subject = '{0}~{1}~FY{2}~({3})'.format(new_due_date.action_id, case, str(fy) ,pnum)
            subject = o_sub
            content = action.description
            start = new_due_date.critical_date
            start_date = start + timedelta(hours=random.randint(12,24))
            end = start_date + timedelta(minutes=30)
            location = 'N/A'
            is_all_day = False
            reminder_minutes = action.lead_time * 10080 # 10,080 minutes per week and lead time is in weeks

            payload = {
                "subject":subject,
                "body": {"contentType": "html", "content":content},
                "start": {
                    "dateTime":start_date.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    "timeZone":"UTC",
                    },
                "end": {
                    "dateTime":end.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    "timeZone":"UTC",
                    },
                "location": {"displayName":location},
                "isReminderOn": True,
                "reminderMinutesBeforeStart":reminder_minutes,
                "isAllDay": is_all_day,
            }
            new_event = create_event(token, payload)

            return redirect(r'appeal_detail_url', case)

        else:
            due_form = add_critical_due_dates_form()

    context['due_form'] = due_form
    context['case_information'] = case_information
    context['case_due_dates'] = case_due_dates
    context['title'] = 'Review Critical Due Dates'

    return render(
        request,
        'app/review_case_critical_due_dates.html',
        context
        )


def appeal_details(request, pk):
    context = initialize_context(request)
    token = get_token(request)

    case_information = get_object_or_404(appeal_master, pk=pk)
    case = case_information.case_number
    case_due_dates = critical_dates_master.objects.filter(case_number__exact=case).order_by('-critical_date')
    case_issues = provider_master.objects.filter(case_number__exact=case).order_by('issue_id')
    count = case_issues.count()

    if case_information.structure == 'INDIVIDUAL':
        provider_information = case_issues[:1]
    else:
        provider_information = case_issues

    form = acknowledge_case_form(request.POST)
    add_issue_form = add_issue(request.POST)

    if request.method =='POST' and 'ackButton' in request.POST:
        if form.is_valid():
            case_information.create_date = form.cleaned_data['acknowledged_date']
            case_information.acknowledged = 'True'
            case_information.save()

            return redirect(r'appeal_detail_url', case)
        else:
            form = acknowledge_case_form()

    elif request.method == 'POST' and 'add_button' in request.POST:
        if add_issue_form.is_valid():
            new_issue = add_issue_form.save(commit=False)
            new_issue.case_number = case
            new_issue.save()

            return redirect(r'appeal_detail_url', case)
        else:
            add_issue_form = add_issue()

    elif request.method == 'POST':
        search_case = request.POST.get('search')

        return redirect(r'appeal_detail_url', search_case)


    context['form'] = form
    context['add_issue_form'] = add_issue_form
    context['case_information'] = case_information
    context['case_due_dates'] = case_due_dates
    context['case_issues'] = case_issues
    context['provider_information'] = provider_information
    context['count'] = count
    context['title'] = 'Appeal Details'

    return render(
        request,
        'app/appeal_detail.html',
        context
        )

def transfer_issue_view(request, pk):
    context = initialize_context(request)
    token = get_token(request)
    issue_to_transfer = get_object_or_404(provider_master, pk=pk)

    trans_form = transfer_issue_form(request.POST)

    if request.method == 'POST':
        if trans_form.is_valid():
            issue_to_transfer.to = str(trans_form.cleaned_data['to_case'])
            issue_to_transfer.to_date = trans_form.cleaned_data['to_date']
            issue_to_transfer.save()

            new_group_prov = provider_master(case_number= issue_to_transfer.to,
                                                provider_number = issue_to_transfer.provider_number,
                                                fiscal_year = issue_to_transfer.fiscal_year,
                                                npr_date = issue_to_transfer.npr_date,
                                                receipt_date = issue_to_transfer.receipt_date,
                                                was_added = issue_to_transfer.was_added,
                                                issue_id = issue_to_transfer.issue_id,
                                                charge_id = issue_to_transfer.charge_id,
                                                amount = issue_to_transfer.amount,
                                                audit_adjustments = issue_to_transfer.audit_adjustments,
                                                sri_staff_id = issue_to_transfer.sri_staff_id,
                                                active_in_appeal_field = issue_to_transfer.active_in_appeal_field,
                                                to = '',
                                                to_date = issue_to_transfer.to_date,
                                                from_field = str(issue_to_transfer.case_number),
                                                agreement = issue_to_transfer.agreement,
                                                agree_note = issue_to_transfer.agree_note,
                                                provider_specific_note = issue_to_transfer.provider_specific_note)

            new_group_prov.save()


            return redirect(r'appeal_detail_url', str(trans_form.cleaned_data['to_case']))
        else:
            trans_form = transfer_issue_form(request.POST)

    context['issue_to_transfer'] = issue_to_transfer
    context['trans_form'] = trans_form

    return render(request, 'app/transfer_issue.html', context)


def charge_master_view(request):
    context = initialize_context(request)
    token = get_token(request)

    all_charge_codes = charge_master.objects.all()

    context['all_charge_codes'] = all_charge_codes

    return render(request, 'app/charge_master.html', context)



# FOR REFERENCE #
'''
def make_dir(request):
    context = initialize_context(request)
    token = get_token(request)

    new_dir_form = make_dir_form(request.POST)

    if request.method == 'POST' and 'make_dir_button' in request.POST:
        if new_dir_form.is_valid():
            type = request.POST.get('type')
            parent = request.POST.get('parent')
            p_num = request.POST.get('p_num')
            issue = request.POST.get('issue')
            fy = request.POST.get('fy')
            c_num = request.POST.get('c_num')



            if type == 'INDIVIDUAL':
                # Goal: S:\3-AP\1-DOCS\INDIVIDUAL\IND~01-0001~2016~XX-XXXX
                new_path = 'S:\\3-AP\\1-DOCS\\{0}\{1}~{2}~{3}~{4}'.format(type, parent, p_num, fy, c_num)
                try:
                    os.mkdir(new_path)
                    # Sucess Message
                    messages.success(request, 'Directory created successfully!')
                    return context
                except:
                    # Directory Already Exists
                    messages.error(request, 'Directory already exsists')
            else:
                # Goal: S:\3-Ap\1-DOCS\GROUP\OPT~2016~XX-XXXX~1~SSI ERR
                issue_abb = issue_master.objects.get(pk=issue).only('abbreviation')
                new_path = 'S:\\3-AP\\1-DOCS\\{0}\{1}~{2}~{3}~{4}~{5}'.format(type, parent,fy,c_num,issue, issue_abb)
                try:
                    os.mkdir(new_path)
                    # Sucess Message
                    messages.success(request, 'Directory created successfully!')
                except:
                    # Directory Already Exists
                    messages.error(request, 'Directory already exsists')



        else:
            new_dir_form = make_dir_form()

    context['new_dir_form'] = new_dir_form

    return context

class new_due_date(TemplateView):
    template_name=""

    def get(self, request, **kwargs):
        context = initialize_context(request)
        form = new_appeal_master_form()
        context['form'] = form
        return render(request, template_name, context)

    def post(self, request):
        context = initialize_context(request)
        form = new_appeal_master_form(request.POST)
        context['form'] = form
        token = get_token(request)

        if form.is_valid():
            subject = request.POST.get('subject')
            content = request.POST.get('content')
            start = request.POST.get('start')
            end = request.POST.get('end')
            location = request.POST.get('location')
            is_all_day = request.POST.get('is_all_day')

            payload = {
                "subject":subject,
                "body": {"contenType": "html", "content":content},
                "start": {
                    "dateTime":start,
                    "timeZone":"UTC",
                    },
                "end": {
                    "dateTime":end,
                    "timeZone":"UTC",
                    },
                "location": {"displayName":location},
                "isAllDay": is_all_day,
                }
            new_event = create_event(token, payload)
            context['new_event'] = (new_event)

            return render(request, template_name, context=context)
        return render(request, "app/event-form.html", context=context)
'''
