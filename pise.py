# Identity Service Engine (ISE) API integrtor: Utilizing ERS
# Author: David Murphy
# Creation: 02-03-2021
import requests
from http.client import HTTPSConnection
import base64
from base64 import b64encode
import urllib.request
import urllib3
urllib3.disable_warnings()
import json
import time
import xml
import os


class pise(object):
    def __init__(self):
        config_file = 'configuration.json'
        self.dir_path = os.path.abspath(__file__)
        self.fpath = os.path.dirname(self.dir_path)
        with open(f'{self.fpath}/{config_file}','r') as f:
                raw_file = f.read()
                config_raw = json.loads(raw_file)
                self.user = config_raw['servers']['ise']['ers_un']
                self.password = config_raw['servers']['ise']['ers_pw']
                self.node = config_raw['servers']['ise']['ise_pan']
        return
    # timestamp
    def timestamp(method):
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = method(*args, **kwargs)
            te = time.time()
            #print 'NOTE: function ({}) ran for {}ms to finish'.format(method.__name__, args, int((te-ts) * 1000))
            print('[I] {} took {}ms to complete.'.format(method.__name__, int((te-ts) * 1000)))
            return result
        return wrapper
    # get request & auth
    @timestamp
    def get(self, path):
        parms = {}
        prox = {}
        creds = str.encode(':'.join((self.user, self.password)))
        encodedAuth = bytes.decode(base64.b64encode(creds))
        requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.Session()
        response = requests.get(url=f'https://{self.node}:9060/ers/{path}', verify=False, params=parms, proxies=prox, headers={'Accept': 'application/json', 'authorization': ' '.join(("Basic",encodedAuth)),})
        if response.status_code == 200 or 202:
            output = json.loads(response.text)
            get_parser(output)
        elif response.status_code != 200 or 202:
            print(response.status_code)
            return
    # post request & auth
    @timestamp
    def post(self, path, json):
        parms = {}
        prox = {}
        creds = str.encode(':'.join((self.user, self.password)))
        encodedAuth = bytes.decode(base64.b64encode(creds))
        requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.Session()
        response = requests.post(url=f'https://{self.node}:9060/ers/{path}', verify=False, proxies=prox, headers={'Accept': 'application/json', 'authorization': ' '.join(("Basic",encodedAuth)), "content-type": "application/json"}, data=json)
        if response.status_code == 200 or 202:
            output = json.loads(response.text)
            post_parser(output)
        elif response.status_code != 200 or 202:
            print(response.status_code)
            return
    # post request & auth
    @timestamp
    def get_parser(self, input):
        print(input)
        self.stuff = input
        return
    # post request & auth
    @timestamp
    def post_parser(self, input):
        print(input)
        self.stuff = input
        return     
    # 
    #   Endpoint and User actions
    #
    # get all internal users
    @timestamp
    def get_internalusers_all(self):
        path = 'config/internaluser/'
        self.get(path)
        return
    # get user by id
    @timestamp
    def get_internalusers_byid(self, userid):
        path = f'config/internaluser/{user}'
        self.get(path)
        return
    # create user
    @timestamp
    def post_createuser(self, userid, email, first, last):
        path = f'config/internaluser/'
        json = """  {{
        "InternalUser" : {{
            "name" : "{}",
            "enabled" : true,
            "email" : "{}",
            "password" : "T3mp4N0w",
            "firstName" : "{}",
            "lastName" : "{}",
            "changePassword" : true,
            "expiryDateEnabled" : true,
            "passwordIDStore" : "Internal Users"
            }}
            }}
            """.format(userid,email,first,last)
        self.post(path, json)
        return
    # get all gueset users
    @timestamp
    def get_guestusers_all(self):
        path = f'config/guestuser/'
        self.get(path)
        return
    # get anc endpoint by id (str)
    @timestamp
    def get_ancendpoint_byid(self, id):
        path = f'config/ancendpoint/{id}'
        self.get(path)
        return
    # get anc endpoint all
    @timestamp
    def get_ancendpoint_all(self):
        path = f'config/ancendpoint/'
        self.get(path)
        return
    # get anc endpoint all
    @timestamp
    def post_ancendpoint_bulk(self):
        path = f'config/ancendpoint/bulk/submit'
        json = {
        "ErsAncEndpointBulkRequest" : {
        "operationType" : "create",
        "resourceMediaType" : "json"
            }
        }
        self.post(path, json)
        return
    # get endpoint by name
    @timestamp
    def get_endpoint_byname(self, name):
        path = f'config/endpoint/name/{name}'
        self.get(path)
        return
    # get rejected endpoints
    @timestamp
    def get_rejected_endpoints_all(self):
        path = f'config/endpoint/getrejectedendpoints'
        self.get(path)
        return
    # DeRegister and endpoint by id (str)
    @timestamp
    def put_deregrister_endpoint_byid(self, id):
        path = f'config/endpoint/{id}/deregister'
        self.post(path)
        return
    # Release Rejected Endpoint
    @timestamp
    def put_release_rejected_endpoint_byid(self, id):
        path = f'config/endpoint/{id}/releaserejectedendpoint'
        self.post(path)
        return
    # Get endpoint by ID (str)
    @timestamp
    def get_endpoint_byid(self, id):
        path = f'config/endpoint/{id}'
        self.get(path)
        return
    # Get endpoint by MAC
    @timestamp
    def get_endpoint_bymac(self, mac):
        path = f'config/endpoint/mac/{mac}'
        self.get(path)
        return
    # Get endpoint all
    @timestamp
    def get_endpoint_all(self):
        path = f'config/endpoint/'
        self.get(path)
        return
    # 
    # ***PSN*** actions
    # 
    @timestamp
    def get_psn_detials_byid(self, id):
        path = f'config/sessionservicenode/name/{id}'
        self.get(path)
        return
    # 
    @timestamp
    def get_psn_detials_byname(self, name):
        path = f'config/sessionservicenode/{name}'
        self.get(path)
        return
    #
    @timestamp
    def get_psn_detials_all(self, name):
        path = f'config/sessionservicenode/'
        self.get(path)
        return
    #
    @timestamp
    def get_psn_detials_verinfo(self, name):
        path = f'config/sessionservicenode/versioninfo'
        self.get(path)
        return
    # 
    # Node detials: PAN, PSN, PMN
    # 
    @timestamp
    def get_node_detials_byname(self, name):
        path = f'config/node/name/{name}'
        self.get(path)
        return
    # 
    @timestamp
    def get_node_detials_byname(self, id):
        path = f'config/node/{id}'
        self.get(path)
        return
    # 
    @timestamp
    def get_node_detials_byid(self, id):
        path = f'config/node/{id}'
        self.get(path)
        return
    # 
    @timestamp
    def get_node_detials_all(self):
        path = f'config/node/'
        self.get(path)
        return
    # 
    @timestamp
    def get_node_detials_verinfo(self):
        path = f'config/node/versioninfo'
        self.get(path)
        return
    # 
    # Native Supplicant Profile
    #     
    @timestamp
    def get_nspprofile_all(self):
        path = f'config/nspprofile'
        self.get(path)
        return 
        

if __name__ == '__main__':
    pise = pise()
    # some example uses of the functions:
    #
    #getmac = pise.get_endpoint_mac('00:00:00:00:00:00')
    #getallusers = pise.get_internalusers_all()
    #getuser = pise.get_internalusers_byid('temp')
    #createuser = pise.post_createuser('Configadmin', 'test@test.com', 'Bob Jones', 'Testing')
    #getguestall = pise.get_guestusers_all()
    #getancendpointbyid = pise.get_endpoint_all()
    # 
