import json
import requests
import logging

class UserClient(object):

    def __init__(self,APIKEY,BASEURL):
        # super(MovieClient, self).__init__()
        self.key = APIKEY
        self.baseURL = BASEURL

    def getReq(self,url):
        try:
            res = requests.get(url)
            return res
        except:
            logging.info("error in get request")