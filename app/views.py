from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from app.graph_helper import get_user, get_calendar_events, create_event
import dateutil.parser
from app.forms import *
from django.views.generic import TemplateView
import datetime
from datetime import datetime
from datetime import date

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

def home(request):
    context = initialize_context(request)

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

"""
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
"""
