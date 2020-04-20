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

base_url = f'https://{cfg["GAT_SUBDOMAIN"]}.gat.digital/api/v2/assets'

asset_types = ['HOST', 'APPLICATION', 'PERSON', 'PROCESS', 'COMPANY', 'CLOUD']

def get_all_assets(size=None, page=None):
    if(size and size > 200):
        return {'err': 'Invalid argument.', 'msg': "'size' must be at most 200."}
    if(not size):
        size = 30
    if(not page):
        page = 0
    return requests.get(url=f'{base_url}?size={size}&page={page}', headers=headers)

def find_asset(key, size=None, page=None):
    if(size and size > 200):
        return {'err': 'Invalid argument.', 'msg': "'size' must be at most 200."}
    if(not size):
        size = 30
    if(not page):
        page = 0
    
    data = {
        'key': [key]
    }
    return requests.post(url=f'{base_url}?size={size}&page={page}', json=data, headers=headers)

def create_asset(**kwargs):
    a_type = kwargs.get('type', None)
    if(not a_type or a_type.upper() not in asset_types):
        return {'err': 'Missing required information.', 'msg': f"type must be one of: {', '.join(asset_types)}"}
    if(not kwargs.get(a_type.lower(), None)):
        return {'err': 'Missing required information.', 'msg': f'Information about {a_type} is needed.'}
    if(not kwargs.get('key', None)):
        return {'err': 'Missing required information.', 'msg': f"'key' is required."}
    
    data = {}
    for arg in kwargs:
        data[arg] = kwargs[arg]
    return requests.put(url=base_url, headers=headers, json=data)