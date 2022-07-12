import requests
from bs4 import BeautifulSoup as bs
import os
from . import header


def isLink(url: str) -> bool:
    return True if url.split('/')[0][:4] == 'http' else False


def pageToHtml(url: str, path: str, debug:bool=True) -> dict:
    """download the page and save it under PATH

    :param url: link of the site page.
    :param path: path to save the html file and its dependencies.
    :param debug: assign logs to logs variable.
    :return: return a dict with three keys: ok, files, logs
    """
    result = {
        'ok': False,
        'files': {
            'styles': [],
            'images': [],
            'scripts': [],
        },
        'logs': '',
    }

    headers = header.headers

    page = requests.get(url, headers=headers)
    domain = url.split('/')[2]
    prefix = f"{url.split('/')[0]}//" if 'www.' in url.split('/')[2] else f'{url.split("/")[0]}//www.'

    if page.status_code != 200:
        result['logs'] += f'site returned {page.status_code} http code'
        return result

    result['ok'] = True
    result['logs'] += '\nrequest to site sent'

    bspage = bs(page.content, 'html.parser')

    result['files']['images'] = [x.get('src') for x in bspage.find_all('img')]
    result['files']['scripts'] = [x.get('src') for x in bspage.find_all('script')]
    result['files']['styles'] = [x.get('href') for x in bspage.find_all('link') if 'stylesheet' in x.get('rel') and x.get('href')]

    result['logs'] += f'\n{len(result["files"]["styles"])} styles find in the page'
    result['logs'] += f'\n{len(result["files"]["images"])} images find in the page'
    result['logs'] += f'\n{len(result["files"]["scripts"])} scripts find in the page'

    for kind in result['files']:
        for i in result['files'][kind]:
            if i:
                if 'data:image' not in i:
                    with open(f'{path}/{os.path.basename(i)}', 'wb') as fli:
                        try:
                            file = requests.get(i, headers=headers) if isLink(i) else requests.get(f'{prefix}{domain}{i}', headers=headers)
                        except:
                            file = requests.get(f'{prefix}{domain}{i}'.replace('www.', ''), headers=headers)
                        if file.status_code == 200:
                            fli.write(file.content)
                            result['logs'] += f'\nfile {i} downloaded'
                        else:
                            result['logs'] += f'\ncould not get the {prefix}{domain}{i}, http code: {file.status_code}'

    for i in ['img', 'script']:
        for j in bspage.find_all(i):
            if j.get('src'):
                if 'data:image' not in j['src']:
                    j['src'] = os.path.basename(j['src'])

    for style in bspage.find_all('link'):
        style['href'] = os.path.basename(style['href']) if style.get('href') else ...

    with open(f'{path}/index.html', 'w') as fli:
        fli.write(str(bspage))

    return result
