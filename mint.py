import yaml
import requests
import json
import csv
import StringIO
import cookielib


class MintCookieException(Exception):
    pass

class MintTokenException(Exception):
    pass

class MintJSONException(Exception):
    pass

class MintWrongTurnException(Exception):
    pass


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
        self.session.cookies.clear()
        headers = {}
        headers["accept"] = "application/json"
        data = {
                "username": self.username, 
                "password": self.password, 
                "task": "L",
                }

        response = self.session.post(self.LOGIN_URL, data=data, headers=headers)

        if len(response.cookies) < 4:
<<<<<<< HEAD
=======
            #raise MintCookieException()
>>>>>>> 27580192d6f99014b583065c441798fb52619cc1
            for c in self.session.cookies:
                if c.name == '_exp_mintPN':
                    if '=' in c.path:
                        true_path, hidden_cookie = c.path.split(',')
                        c.path = true_path
                        new_cookie_name, new_cookie_value = hidden_cookie.split('=')
                        new_cookie = {}
                        cookie_attributes = ['version', 'port', 'port_specified', 'domain', \
                                'domain_specified', 'domain_initial_dot', 'path', 'path_specified', \
                                'secure', 'expires', 'discard', 'comment', 'comment_url', 'rfc2109']
                        for attr in cookie_attributes:
                            new_cookie[attr] = getattr(c, attr)
                        new_cookie['name'] = 'MINTJSESSIONID'
                        new_cookie['value'] = new_cookie_value
                        new_cookie['rest'] = {}
                        new_cookie = cookielib.Cookie(**new_cookie)
                        self.session.cookies.set_cookie(new_cookie)

        if 'token' not in response.text:
            raise MintTokenException()

        resjson = json.loads(response.text)
        if not resjson["sUser"]["token"]:
            raise MintJSONException
        else:
            self.token = resjson["sUser"]["token"]
        return response

    def get_csv(self):
        if not self.token:
            self.login()
        #params = {'queryNew': '', 'offset': '0', 'accountId': '6677642', 'comparableType': '8'}
        params = {'queryNew': '', 'offset': '0', 'comparableType': '8'}
        response = self.session.get(self.CSV_URL, params=params)
        if 'Perhaps you took a wrong turn' in response.text:
            raise MintWrongTurnException
        return response.text

#mint = Mint()
#mint.get_csv()
