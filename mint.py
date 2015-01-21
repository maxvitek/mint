import yaml
import requests
import json
import csv
import StringIO


class Mint(object):
    '''
    mint.com interface
    '''
    BASE_URL  = 'https://wwws.mint.com'
    LOGIN_URL = '{0}/loginUserSubmit.xevent'.format(BASE_URL)
    CSV_URL   = '{0}/transactionDownload.event'.format(BASE_URL)

    def __init__(self, username=None, password=None):
        if not username or not password:
            self.config = yaml.load(open('config.yaml', 'r'))
        if username:
            self.username = username
        else:
            self.username = self.config['username']
        if password:
            self.password = password
        else:
            self.password = self.config['password']
        self.token = None
        self.session = requests.Session()

    def login(self):
        headers = {}
        headers["accept"] = "application/json"
        data = {
                "username": self.username, 
                "password": self.password, 
                "task": "L",
                }

        response = self.session.post(self.LOGIN_URL, data=data, headers=headers)
        
        if 'token' not in response.text:
            raise Exception("Mint.com login failed[1]")

        resjson = json.loads(response.text)
        if not resjson["sUser"]["token"]:
            raise Exception("Mint.com login failed[2]")
        else:
            self.token = resjson["sUser"]["token"]
        return response

    def get_csv(self):
        if not self.token:
            self.login()
        params = {'queryNew': '', 'offset': '0', 'accountId': '6677642', 'comparableType': '8'}
        response = self.session.get(self.CSV_URL, params=params)
        if 'Perhaps you took a wrong turn' in response.text:
            raise Exception('Mint.com hates you')
        return response.text

#mint = Mint()
#mint.get_csv()
