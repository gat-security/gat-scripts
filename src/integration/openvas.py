import sys
import csv
import os
import logging

from gat_api import issues, assets

columns = {
    'A': 'IP',
    'B': 'Hostname',
    'C': 'Port',
    'D': 'Port Protocol',
    'E': 'CVSS',
    'F': 'Severity',
    'G': 'Solution Type',
    'H': 'NVT Name',
    'I': 'Summary',
    'J': 'Specific Result',
    'K': 'NVT OID',
    'L': 'CVEs',
    'M': 'Task ID',
    'N': 'Task Name',
    'O': 'Timestamp',
    'P': 'Result ID',
    'Q': 'Impact',
    'R': 'Solution',
    'S': 'Affected Software/OS',
    'T': 'Vulnerability Insight',
    'U': 'Vulnerability Detection Method',
    'V': 'Product Detection Result',
    'W': 'BIDs',
    'X': 'CERTs',
    'Y': 'Other References'
}

issue_severity = {
    'critical': 4,
    'high': 3,
    'medium': 2,
    'low': 1,
    'log': 0
}

TOTAL_ASSETS_ON_FILE = 0
TOTAL_ISSUES_ON_FILE = 0
ASSETS_CREATED = 0
ASSETS_SKIPPED = 0
ISSUES_CREATED = 0
ISSUES_UPDATED = 0
ISSUES_SKIPPED = 0

def my_progress(count, total, status=''):
    bar_len = 60
    fille_len = int(round(bar_len * count / float(total)))

    bar = '=' * fille_len + '-' * (bar_len - fille_len)

    sys.stdout.write(f'[{bar}] {count} out of {total}    {status}\r')
    sys.stdout.flush()

def open_file(filename):
    if(not filename):
        filename = input('Por favor, escreva o caminho completo do arquivo:\n')
    
    path = os.path.dirname(filename) + '/openvas.log'

    if(filename.split('.')[-1].lower() != 'csv'):
        filename = filename + '.csv'
    
    try:
        logging.basicConfig(filename=path, format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
        openvas_file = open(filename, 'r')
    except FileNotFoundError:
        print('O arquivo não foi encontrado, verifique o caminho e o nome do arquivo e tente novamente.')
        sys.exit(1)
    return csv.DictReader(openvas_file, delimiter=','), path

def review(log_file=''):
    width, height = os.get_terminal_size()
    c = int(width / 2)
    print('+='*c)
    print('\n')
    print(f'\tTotal number of Assets on file: {TOTAL_ASSETS_ON_FILE}')
    print(f'\tTotal number of Issues on file: {TOTAL_ISSUES_ON_FILE}')
    print(f'\tTotal number of Assets created: {ASSETS_CREATED}')
    print(f'\tTotal number of Assets skipped: {ASSETS_SKIPPED}')
    print(f'\tTotal number of Issues created: {ISSUES_CREATED}')
    print(f'\tTotal number of Issues updated: {ISSUES_UPDATED}')
    print(f'\tTotal number of Issues skipped: {ISSUES_SKIPPED}')
    print('\n')
    print(f'\tFor more information, check the log on: {log_file}')
    print('\n')
    print('+='*c)

def modify_file(openvas):
    global TOTAL_ASSETS_ON_FILE
    global TOTAL_ISSUES_ON_FILE
    assets = set()
    line_count = 0
    new = []
    for row in openvas:
        if(line_count == 0):
            line_count += 1
            continue
        assets.add(row[columns['A']])
        row[columns['F']] = issue_severity[row[columns['F']].lower()]
        if(row[columns['C']] == ''):
            row[columns['C']] = '0'
        if(row[columns['D']] == ''):
            row[columns['D']] = 'tcp'
        if(row[columns['R']] == ''):
            row['Solution Title'] = ''
        else:
            row['Solution Title'] = row[columns['H']]
        if(row[columns['L']] != ''):
            cves = row[columns['L']].split(',')
            cve_count = len(cves)
            for i in range(cve_count):
                row['CVE'+str(i+1)] = cves[i]

        row['Ferramenta'] = 'OPENVAS'
        new.append(row)
        line_count += 1
    TOTAL_ASSETS_ON_FILE = len(assets)
    TOTAL_ISSUES_ON_FILE = line_count - 1
    return new

def create_asset(row, row_number):
    global ASSETS_CREATED
    global ASSETS_SKIPPED

    asset_data = {
        'type': 'HOST',
        'key': row[columns['A']],
        'host': {
            'type': 'workstation'
        }
    }
    if(row[columns['B']]):
        asset_data['host'] = {'hostname': row[columns['B']]}
    
    r = assets.create_asset(**asset_data)
    
    if(r.status_code == 201):
        ASSETS_CREATED += 1
        new_asset = r.json()
        result = {'entity': 'asset', 'row_number': str(row_number), 'type': 'create', 'result': 'success', 'asset_id': new_asset['asset_id']}
        logging.info(result)
        return new_asset
    else:
        ASSETS_SKIPPED += 1
        result = {'entity': 'asset', 'row_number': str(row_number), 'type': 'create', 'result': 'fail', 'status_code': str(r.status_code)}
        logging.info(result)
        return r.status_code

def find_or_create_asset(row, row_number):
    global ASSETS_SKIPPED

    # Check if the Asset already exists on GAT
    a = assets.find_asset(row[columns['A']])

    if(a.status_code == 200):
        asset = a.json()['content'][0]
        result = {'entity': 'asset', 'row_number': str(row_number), 'type': 'found', 'result': 'success', 'asset_id': asset['asset_id']}
        logging.info(result)
        return asset
    
    # if not, try to create it
    elif(a.status_code == 204):
        return create_asset(row, row_number)

def create_issue(row, asset, row_number):
    global ISSUES_CREATED
    global ISSUES_SKIPPED

    issue_data = {
        'title': row[columns['H']],
        'asset': {'asset_id': asset.get('asset_id')},
        'port': int(row[columns['C']]),
        'protocol': row[columns['D']],
        'severity': row[columns['F']],
        'description': row[columns['I']]
    }
    r = issues.create_issue(**issue_data)
    if(r.status_code == 201):
        new_issue = r.json()
        ISSUES_CREATED += 1
        result = {'entity': 'issue', 'row_number': str(row_number), 'type': 'create', 'result': 'success', 'issue_id': new_issue['issue_id'], 'asset_id': asset['asset_id']}
        logging.info(result)
        return result
    else:
        ISSUES_SKIPPED += 1
        result = {'entity': 'issue', 'row_number': str(row_number), 'type': 'create', 'result': 'fail', 'status_code': r.status_code}
        logging.info(result)
        return result

def update_issue(issue_id, data, asset_id, row_number):
    global ISSUES_UPDATED
    global ISSUES_SKIPPED

    # Update the existing Issue
    r = issues.update_issue(issue_id, **data)
    if(r.status_code == 201):
        updated_issue = r.json()
        ISSUES_UPDATED += 1
        result = {'entity': 'issue', 'row_number': str(row_number), 'type': 'update', 'result': 'success', 'issue_id': updated_issue['issue_id'], 'asset_id': asset_id}
        logging.info(result)
        return result
    else:
        ISSUES_SKIPPED += 1
        result = {'entity': 'issue', 'row_number': str(row_number), 'type': 'update', 'result': 'fail', 'status_code': r.status_code}
        logging.info(result)
        return result

def search_issue(row, asset, row_number):
    global ISSUES_SKIPPED

    # Search matching Issue+Asset
    search_issue = {
        'title': [row[columns['H']]],
        'asset_id': [asset.get('asset_id')]
    }

    # Check is this Issue already exists on GAT
    i = issues.find_issue(**search_issue)

    # If it exists, update its Status
    if(i.status_code == 200):
        found_issues = i.json()['content']

        if(len(found_issues) == 1):
            issue = found_issues[0]
        elif(len(found_issues) > 1):
            found = False
            for found_issue in found_issues:
                if(found_issue['port'] == int(row[columns['C']]) and found_issue['protocol'] == row[columns['D']]):
                    issue = found_issue
                    found = True
                    break
            if(not found):
                ISSUES_SKIPPED += 1
                result = {'entity': 'issue', 'row_number': str(row_number), 'type': 'update', 'result': 'fail', 'msg': 'Too many Issues found!', 'issues': found_issues}
                logging.info(result)
                return result
        
        # Issue found
        issue_id = issue['issue_id']
        if(issue['status'] == 'PENDING'):
            data = {
                'status': 'PENDING'
            }
        else:
            data = {
                'status': 'REOPENED'
            }
        update_issue(issue_id, data, asset['asset_id'], row_number)

        return True
    return False

def find_or_create_issue(row, row_number):
    asset = find_or_create_asset(row, row_number)
    if(type(asset) == type(1)):
        return

    if(not search_issue(row, asset, row_number)):
        create_issue(row, asset, row_number)

def main(filename=None):
    openvas, log_file = open_file(filename)
    openvas_modified = modify_file(openvas)
    line_count = 0
    for row in openvas_modified:
        my_progress(line_count, TOTAL_ISSUES_ON_FILE)
        line_count += 1
        find_or_create_issue(row, line_count)
    review(log_file)