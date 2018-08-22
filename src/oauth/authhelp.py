#from urllib.parse import quote, urlencode

from django.utils.http import urlencode
import requests
import base64
import json
import time
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'
# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{0}'
# The token issuing endpoint
token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# The scopes required by the app
scopes = [ 'openid',
           'User.Read',
           'offline_access',
           'Mail.Read' ]

def get_signin_url(redirect_uri):
  # Build the query parameters for the signin url
  params = { 'client_id': client_id,
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'scope': ' '.join(str(i) for i in scopes)
            }

  signin_url = authorize_url.format(urlencode(params))

  return signin_url

def get_token_from_code(auth_code, redirect_uri):
  # Build the post form for the token request
  post_data = { 'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }
  #using the constant url "token url" to post the required data along with the auth_code
  r = requests.post(token_url, data = post_data)
  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_token_from_request_token(request_token, redirect_uri):
    #build the post form for the token
    post_data = {
            "grant_type" : "refresh_token",
            "refresh_token" : refresh_token,
            "redirect_uri" : redirect_uri,
            'scope' : ' '.join(str(i) for i in scopes),
            'client_id' : client_id,
            'client_secret' : client_secret,
    }

    requests.post(token_url, data = post_data)
    try:
        return r.json()
    except:
        return "Error retrieving token from request token {0} - {1}".format(r.status_code, r.text)

def get_access_token(request, redirect_uri):
    current_token = request.session["access_token"]
    expiration  = request.session["token_expires"]
    now = int(time.time())
    if (current_token and now < expiration):
        return current_token
    else:
        refresh_token = request.session["refresh_token"]
        new_token = get_token_from_request_token(refresh_token, redirect_uri)
        expiration = int(time.time()) + expires_in - 120

        #saving the session
        
        
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session['token_expires'] = expiration
        return new_token["access_token"]
