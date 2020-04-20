import csv
import sys

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

def open_file():
    if(len(sys.argv) == 1):
        f = input('Por favor, escreva o caminho completo do arquivo:\n')
    else:
        f = sys.argv[1]
    
    if(f.split('.')[-1].lower() != 'csv'):
        f = f + '.csv'

    try:
        openvas_file = open(f, 'r')
    except FileNotFoundError:
        print('O arquivo não foi encontrado, verifique o caminho e o nome do arquivo e tente novamente.')
        sys.exit(1)
    return csv.DictReader(openvas_file, delimiter=','), f

def modify_file(openvas):
    line_count = 0
    new = []
    for row in openvas:
        if(line_count == 0):
            line_count += 1
            continue
        if(row[columns['C']] == ''):
            row[columns['C']] = '0'
        if(row[columns['D']] == ''):
            row[columns['D']] = 'tcp'
        if(row[columns['F']] == 'Log'):
            row[columns['F']] = 'Info'
        if(row[columns['R']] == ''):
            row['Solution Title'] = ''
        else:
            row['Solution Title'] = row[columns['H']]
        if(row[columns['L']] != ''):
            cves = row[columns['L']].split(',')
            cve_count = len(cves)
            for i in range(cve_count):
                row['CVE'+str(i+1)] = cves[i]
        del row[columns['L']]

        row['Ferramenta'] = 'OPENVAS'
        new.append(row)
    return new

def create_file(openvas, header, filename):
    f = filename.split('.')
    f[-2] = f[-2] + '_mod'
    filename = '.'.join(f)
    #print(openvas)
    with open(filename, mode='w') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=header)

        writer.writeheader()
        writer.writerows(openvas)


if __name__ == '__main__':
    openvas, filename = open_file()
    openvas_modified = modify_file(openvas)
    l = 0
    for i in openvas_modified:
        if(len(i) > l):
            l = len(i)
            header = i.keys()
    print(header)
    create_file(openvas_modified, header, filename)