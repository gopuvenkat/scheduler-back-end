#from urllib.parse import quote, urlencode

from django.utils.http import urlencode
import requests
import base64
import json
import time

client_id = '9c474603-bb4b-4a2b-95f2-0764dabb66d6'
client_secret = 'jcexXPFSL543%!]kvoNE52|'

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
