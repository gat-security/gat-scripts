import sys
import subprocess
import pkg_resources

required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print(f'Installing dependencies: {missing}...')
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    print('\nDone!')

import requests

from .config import config as cfg

headers = {
    'Authorization': cfg['GAT_API_KEY'],
    'Content-Type': 'application/json'
}

base_url = f'https://{cfg["GAT_SUBDOMAIN"]}.gat.digital/api/v1/issues'

def get_all_issues(size=None, page=None):
    if(size and size > 200):
        return {'err': 'Invalid argument.', 'msg': "'size' must be at most 200."}
    if(not size):
        size = 30
    if(not page):
        page = 0
    
    return requests.get(url=f'{base_url}?size={size}&page={page}', headers=headers)

def find_issue(size=None, page=None, **kwargs):
    if(size and size > 200):
        return {'err': 'Invalid argument.', 'msg': "'size' must be at most 200."}
    if(not size):
        size = 30
    if(not page):
        page = 0
    
    data = {}
    for arg in kwargs:
        data[arg] = kwargs[arg]
    return requests.post(url=f'{base_url}?size={size}&page={page}', json=data, headers=headers)

def create_issue(**kwargs):
    if(not kwargs['title']):
        return {'err': 'Missing required information.', 'msg': f"'title' is required."}
    if(not kwargs['asset']):
        return {'err': 'Missing required information.', 'msg': f"'asset' is required."}
    
    data = {}
    for arg in kwargs:
        data[arg] = kwargs[arg]
    return requests.put(url=base_url, json=data, headers=headers)

def update_issue(id, **kwargs):
    data = {}
    for arg in kwargs:
        data[arg] = kwargs[arg]
    return requests.patch(url=f'{base_url}/{id}', json=data, headers=headers)