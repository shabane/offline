from django.shortcuts import render
import os
import requests
from .models import Paper, User
from bs4 import BeautifulSoup as bs
from hashlib import blake2b
from . import moduls

def index(request):
    lst = []
    if request.user.is_authenticated:
        user = request.user
        if not os.path.exists(f'offpages/{user}'):
            os.mkdir(f'offpages/{user}')
        lst = Paper.objects.filter(owner=user)[::-1]

    context = {'pages': lst}
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'error.html', {'error': 'you are not authenticated, pleas login first'})
        url = request.POST.get('url')
        site = requests.get(url)

        if site.status_code != 200 and site.status_code != 403:
            return render(request, 'error.html', {'error': f'the url which you provide cant be reached, code: {site.status_code}'})

        page = bs(site.content, 'html.parser')
        title = page.title.contents[0]
        dir_name = blake2b(bytes(title, encoding='utf-8')).hexdigest()[::10]

        if not os.path.exists(f'offpages/{user}/{dir_name}'):
            os.mkdir(f'offpages/{user}/{dir_name}')

        result = moduls.pageToHtml(url, f'offpages/{user}/{dir_name}')

        if not result['ok']:
            return render(request, 'error.html', {'error': result['logs']})

        Paper.objects.create(owner=user, title=title, url=url, path=f'{user}/{dir_name}/index.html')

    return render(request, 'index.html', context)
