# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import datetime
import pytz
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth.authhelp import get_signin_url, get_token_from_code, get_access_token
from oauth.outlookservice import get_me, get_my_messages
from models import Emails, Users
from oauth.serializers import homeSerializer, UserSerializer, tokenSerializer
from rest_framework import views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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
    #npuser = new_possible_user
    npuser = Users()
    global current_user
    current_user = user['mail']
    npuser.email = user['mail']
    npuser.username = user['displayName']
    try:
        npuser.save()
    except:
        pass
    return HttpResponseRedirect(reverse('oauth:token'))

def mail(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('oauth:gettoken')))
    # If there is no token in the session, redirect to home
    global current_user
    current_user_obj = Users.objects.get(email=current_user)
    if not access_token:
        return HttpResponseRedirect(reverse('oauth:home'))
    else:
        message = get_my_messages(access_token)
        time_now = datetime.datetime.utcnow()
        for i in range(10):
            #rt = received time
            todo = Emails()
            todo.username = current_user_obj
            rt = message['value'][i]['receivedDateTime']
            rt_dt = datetime.datetime(int(rt[0:4]), int(rt[5:7]), int(rt[8:10]), int(rt[11:13]), int(rt[14:16]), int(rt[17:19]),0,pytz.UTC)
            if (rt_dt > current_user_obj.lastchecked):
                todo.receivedDateTime = rt_dt
                todo.title = message['value'][i]['body']['content']
                todo.date = rt_dt.date()
                todo.start_time = rt_dt.time()
                todo.end_time = rt_dt.time()
                todo.save()
        current_user_obj.lastchecked = datetime.datetime.utcnow()
        current_user_obj.save()
        return current_user

def token(request):
    global current_user
    current_user_object = Users.objects.get(email=current_user)
    token = Token.objects.get_or_create(user=current_user_object)
    return token[0]

class tokenView(views.APIView):
    def get(self, request):
        mail(request)
        data = {'token' : token(request)}
        results = tokenSerializer(data).data
        return Response(results)


class mailView(views.APIView):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
         user = mail(request)
         queryset = Emails.objects.filter(username__email = user)
         id = Users.objects.get(email=user).pk
         data = {'id' : id, 'email' : user, 'mails' : Emails.objects.filter(username__email = user)}
         results = UserSerializer(data).data
         return Response(results)
