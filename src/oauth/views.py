# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from oauth.authhelp import *
from oauth.outlookservice import *

def home(request):
    redirect_uri = request.build_absolute_uri(reverse("oauth:gettoken"))
    sign_in_url = get_signin_url(redirect_uri)
    print redirect_uri
    return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
    auth_code = request.GET["code"]
    redirect_uri = request.build_absolute_uri(reverse("oauth:gettoken"))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token["access_token"]
    user = get_me(access_token)

    #saving the session
    request.session['access_token'] = access_token
    return HttpResponse("User Name : {0}  Access Token : {1}".format(user["displayName"], access_token))
