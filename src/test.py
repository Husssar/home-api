import cred
import requests
from requests.adapters import HTTPAdapter
import urllib3
from urllib3 import Retry
import time
import sys
URL = f'http://{cred.TEST_URL}'
OK = True
NOK = False

def print_result(text, status):
    print(f'{text}\t [  {status}  ]')

def test_start():
    response = requests.get(URL).json()
    status = False
    if response['welcome'] == 1337:
        status = OK
    print_result('TESTING START PAGE', status)
        
def get_temperature(meter_no, layer):
    extended_url = f'/temperature/{meter_no}/{layer}'
    response = requests.get(URL + extended_url).json()
    txt = f'TESTING TEMPERATURE FOR {meter_no}'
    status = NOK
    if response['temperature'] != None:
        status = OK
    print_result(txt, status)


def get_graph():
    extended_url = f'/static/images/test.png?rand=0.1337'
    response = requests.get(URL + extended_url)
    status = NOK
    if response.status_code == 200:
        status = OK
    print_result('Grapg was generated', status)

def get_date():
    extended_url = f'/date/'
    response = requests.get(URL + extended_url).json()

def wait_for_backend():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=Retry(total=4, backoff_factor=1, allowed_methods=None))
    session.mount("http://", adapter)
    start_time = time.monotonic()
    try:
      r = session.get(URL)
      print(r.status_code)
      if r.status_code == 200:
          print("Backend up'n running, let's start!")
    except Exception as e:
        print(e)
        stop_time = time.monotonic()
        print(round(stop_time-start_time,2), "seconds")
        print("Backend failure, no need to start tests")
        sys.exit(1)


def main():
    wait_for_backend()
    test_start()
    get_temperature('63006338', 'ext-temp')
    get_graph()
    get_date()

main()

