import logging
import requests
import json
from termcolor import colored
from colorama import init
init(autoreset = True)

apiKey = 'API KEY HERE'     # Insert your API key here
selector = "Google"   # Insert the DKIM selector here
domain = 'www.google.com'     # Insert the domain URL here

# LOGGER CONFIG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO)
console_format = logging.Formatter('[%(asctime)s] %(levelname)-8s - %(message)s')
console_log.setFormatter(console_format)
logger.addHandler(console_log)

def query_api(logger, apikey, command, domain, selector=None):
    logger.debug('Entering query_api')
    
    url = f'https://mxtoolbox.com/api/v1/Lookup/{command}/{domain}'
    if command == 'DKIM':
        if not selector:
            selector = 'google'  # Default selector
        url = f'https://mxtoolbox.com/api/v1/Lookup/{command}/?argument={domain}:{selector}'
    headers = {'Authorization': apikey}
    logger.debug(f'Trying API request for {domain} with {command}')
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f'API request error: {e}')
        raise
    logger.debug('Finished making API request')
    data = r.text
    return data

def print_result(name, status, color):
    print(f'{colored(name, color)}: {status}')

def print_section_title(title):
    print(colored(title, attrs=['bold']))

print(colored(domain, 'magenta'))
commands = ['SPF', 'DMARC', 'DKIM']  # List of commands to execute

for c in commands:
    print_section_title(c)
    data = query_api(logger, apiKey, c, domain, selector)
    resp_dict = json.loads(data)
    
    if c == 'DKIM':
        if resp_dict.get('DKIMRecord'):
            print_result('DKIM Record Published', 'Yes', 'green')
        else:
            print_result('DKIM Record Published', 'No DKIM Record found', 'red')
    
    else:
        for p in resp_dict['Failed']:
            print_result(p['Name'], p['Info'], 'red')
        
        for p in resp_dict['Warnings']:
            print_result(p['Name'], p['Info'], 'yellow')
        
        for p in resp_dict['Passed']:
            print_result(p['Name'], p['Info'], 'green')
        
        for p in resp_dict['Information']:
            print(json.dumps(p))
        
    print("-------------------------")
