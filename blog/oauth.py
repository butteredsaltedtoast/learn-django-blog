import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

def ion_login(request):
    url = (
        'https://ion.tjhsst.edu/oauth/authorize/'
        f'?response_type=code'
        f'&client_id={settings.ION_CLIENT_ID}'
        f'&redirect_uri={settings.ION_REDIRECT_URI}'
        f'&scope=read'
    )
    return redirect(url)

def ion_callback(request):
    code = request.GET.get('code')
    token_response = requests.post('https://ion.tjhsst.edu/oauth/token/', data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.ION_REDIRECT_URI,
        'client_id': settings.ION_CLIENT_ID,
        'client_secret': settings.ION_CLIENT_SECRET,
    })
    access_token = token_response.json().get('access_token')
    profile = requests.get('https://ion.tjhsst.edu/api/profile', headers = {
        'Authorization': f'Bearer {access_token}',
    }).json()
    username = profile.get('ion_username')
    user, created = User.objects.get_or_create(username=username)
    login(request, user)
    return redirect('post_list')

def ion_logout(request):
    logout(request)
    return redirect('post_list')