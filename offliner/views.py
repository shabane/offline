from django.shortcuts import render
from django.http import HttpResponse
import os
import requests

def index(request):
    lst = [
        {
            'link': 'https://google.com',
            'title': 'this is google page'
        },
        {
            'link': 'https://google.com',
            'title': 'this is another page'
        }
    ]
    context = {'pages': lst}
    if request.method == 'POST':
        url = request.POST.get('url')
        if requests.get(url).status_code != 200:
            return render(request, 'error.html', {'error': 'the url which you provide cant be reached'})
        os.system(f'cd offpages && wget -E -H -k -p {url}')
    return render(request, 'index.html', context)
