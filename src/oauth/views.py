# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from oauth.authhelp import *
from oauth.outlookservice import *
from oauth.serializers import homeSerializer
from rest_framework import views, generics
from rest_framework.response import Response


def signin(request):
    redirect_uri = request.build_absolute_uri(reverse("oauth:gettoken"))
    sign_in_url = get_signin_url(redirect_uri)
    return sign_in_url

class home(views.APIView):
    def get(self, request):
        data = {'sign_in_url' : signin(request)}
        results = homeSerializer(data).data
        return Response(results)

def gettoken(request):
    auth_code = request.GET["code"]
    redirect_uri = request.build_absolute_uri(reverse("oauth:gettoken"))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token["access_token"]
    user = get_me(access_token)
    refresh_token = token["refresh_token"]

    #expires_in is in seconds
    expires_in = token["expires_in"]

    expiration = int(time.time()) + expires_in - 120

    #saving the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    return HttpResponseRedirect(reverse('oauth:mail'))

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('oauth:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('oauth:home'))
  else:
      message = get_my_messages(access_token)
      #a basic json response will be printed on screen
      return HttpResponse('The latest email recieved : {0}'.format(message))
