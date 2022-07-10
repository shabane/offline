import requests
from bs4 import BeautifulSoup as bs
import os


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


    page = requests.get(url)

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
                with open(f'{path}/{os.path.basename(i)}', 'wb') as fli:
                    file = requests.get(i)
                    if file.status_code == 200:
                        fli.write(file.content)
                        result['logs'] += f'\nfile {i} downloaded'
                    else:
                        result['logs'] += f'\ncould not get the {i}'
