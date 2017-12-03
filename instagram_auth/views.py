import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import uuid
import os
import ssl
import sys
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.middleware import get_user # XXX
from django.shortcuts import render, redirect
from instagram.client import InstagramAPI
from instagram_auth.models import AccessToken


def login_instagram(request):
    host = request.get_host()
    if ':' in host: # nginx
        host, _ = host.split(':')

    instagram_url = os.environ.get('INSTAGRAM')
    redirect_uri = f"{host}/accounts/login_instagram/"

    # user authorizes app
    code = request.GET.get('code')
    if code is not None:
        CONFIG = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8515/oauth_callback'
        }
        unauthenticated_api = InstagramAPI(**CONFIG)
        oauth_token = unauthenticated_api.exchange_code_for_access_token(code)
        instagram_account = oauth_token['user']['username']
        if not AccessToken.objects.filter(uid=instagram_account).exists():
            # no access_token found XXX
            AccessToken.objects.create(uid=instagram_account, access_token=oauth_token['access_token'])
        user = authenticate(uid=instagram_account)
        if user is not None:
            auth_login(request, user)
        return redirect('/')

    client_secret = os.environ.get('CLIENT_SECRET')
    url = "https://" + instagram_url + \
        "/oauth/authorize/?client_id=" + client_secret + "&redirect_uri=" + \
        redirect_uri + "&response_type=code&scope=basic+public_content+follower_list+relationships+likes'"
    return redirect(url)

def exchange_CODE_for_ACCESS_TOKEN(instagram_url, redirect_uri, code):
    url = f'https://{instagram_url}/oauth/access_token'
    tmp = urlencode({
        'client_id': 'XXX',
        'client_secret': 'XXX',
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code,
    })
    cnt = ssl.SSLContext(ssl.PROTOCOL_SSLv23) # ignore CERTIFICATE_VERIFY_FAILED
    cnt.verify_mode = ssl.CERT_NONE
    str = urlopen(Request(url, tmp.encode()), context=cnt).read().decode()
    return json.loads(str)

def logout(request):
    auth_logout(request)
    user = get_user(request)
    token = AccessToken.objects.get(uid=user.instagram_account)
    return redirect('/')
