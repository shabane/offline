from django.shortcuts import render
import os
import requests
from .models import Paper, User
from bs4 import BeautifulSoup as bs
from hashlib import blake2b
import subprocess

def index(request):
    lst = []
    if request.user.is_authenticated:
        user = request.user
        if not os.path.exists(f'offpages/{user}'):
            os.mkdir(f'offpages/{user}')
        lst = Paper.objects.filter(owner=user)[::-1]

    context = {'pages': lst}
    if request.method == 'POST':
        url = request.POST.get('url')
        site = requests.get(url)
        domain = url.split('/')[2]

        if site.status_code != 200 and site.status_code != 403:
            return render(request, 'error.html', {'error': f'the url which you provide cant be reached, code: {site.status_code}'})

        page = bs(site.content, 'html.parser')
        title = page.title.contents[0]
        dir_name = blake2b(bytes(title, encoding='utf-8')).hexdigest()[::10]

        if not os.path.exists(f'offpages/{user}/{dir_name}'):
            os.mkdir(f'offpages/{user}/{dir_name}')

        files = list(os.listdir(f'offpages/{user}/{dir_name}'))
        file_name = 'index.html' if 'index.html' in files else os.path.basename(url)+'.html'


        if not os.system(f'cd offpages/{user}/{dir_name} && wget -nd -c -E -H -k -p {url}'):
            return render(request, 'error.html', {'error': 'site could not download'})

        Paper.objects.create(owner=user, title=title, url=url, path=f'{user}/{dir_name}/{file_name}')

    return render(request, 'index.html', context)
