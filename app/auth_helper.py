import os
import time

# This is necessary for testing with non-HTTPS localhost
# Remove this if deploying to production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This is necessary because Azure does not garuntee
# to return scopes in the same case and order as requested
os.environ['OAUTHLIB_RELAX_TOKEN'] = '1'
os.environ['OAUTHLIB_IGNORE_SCOPE_CHANGE'] = '1'

# Load the oauth_settings.yml file
stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, yaml.SafeLoader)
authorize_url = '{0}{1}'.format(settings['authority'], settings['authorize_endpoint'])
token_url = '{0}{1}'.format(settings['authority'], settings['token_endpoint'])

# Method to generate a sign in url
def get_sign_in_url():
    # initialize the OAuth Client
    aad_auth = OAuth2Session(settings['app_id'],
                    scope=settings['scopes'],
                    redirect=settings['redirect'])

    sign_in_url, state = aad_auth.authorization_url(authorize_url, prompt='login')

    return sign_in_url, state

# method to exchange auth coe for access token
def get_token_from_code(callback_url, expected_state):
    # initialize the OAuth Client
    aad_auth = OAuth2Session(settings['app_id'],
                    scope=settings['scopes'],
                    redirect=settings['redirect'])

    token = aad_auth.fetch_token(token_url,
                    client_secret=settings['app_secret'],
                    authorization_response=callback_url)

    return token

def store_token(request, token):
    request.session['oauth_token'] = token

def store_user(request, user):
    request.session['user'] = {
        'is_authenticated':True,
        'name': user['displayName'],
        'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName']
    }

def get_token(request):
    token = request.session['oauth_token']
    if token != None:
        # Check Expiration
        now = time.time()
        # Subtract 5 minutes for Expiration to account to clock skew
        expire_time = token['expires_at'] - 300
        if now >= expire_time:
            # refresh token_endpoin
            aad_auth = OAuth2Session(settings['app_id'],
                            scope=settings['scopes'],
                            redirect=settings['redirect'])

            refresh_params = {
                'client_id': settings['app_id'],
                'client_secret':settings['app_secret'],
            }

            new_token = aad_auth.refresh_token(token_url, **refresh_params)

            # save new token
            store_token(request, new_token)

            # return new token
            return new_token

        else:
            return token

def remove_user_and_token(request):
    if 'oauth_token' in request.session:
        del request.session['oauth_token']

    if 'user' in request.session:
        del request.session['user']