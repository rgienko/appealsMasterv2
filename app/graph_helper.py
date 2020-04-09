from requests_oauthlib import OAuth2Session

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
    graph_client = OAuth2Session(token=token)
    # Send Get to /me
    user = graph_client.get('{0}/me'.format(graph_url))
    # Return the JSON result
    return user.json()

def get_calendar_events(token):
    graph_client = OAuth2Session(token=token)

    # Configure query parameters #
    # modify the results
    query_params = {
        '$select': 'subject, organizer, start, end',
        '$orderby': 'createdDateTime DESC'
    }

    # send Get to /me/events
    events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)

    return events.json()

def create_event(token, payload, **kargs):
    graph_client = OAuth2Session(token=token)
    url_endpoint = "https://graph.microsoft.com/v1.0/me/events"
    new_event = graph_client.post(url=url_endpoint, json=payload)

    return new_event.json()
