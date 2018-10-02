import json

import requests


class instagramweb:
    url = ' https://www.instagram.com/'
    def __init__(self):
        self.s = requests.Session()
        self.request("")

    def request(self, endpoint, data=None, post=False):
        # if (not self.isLoggedIn):
        #     raise Exception("Not logged in!\n")
        #     return

        self.s.headers.update({
            'Host': 'www.instagram.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'DNT': '1',
            'Accept-Language': 'en-US,en;q=0.8',
        })

        try:
            if (post):  # POST
                # response = self.s.post(self.url + endpoint, data=post)  # , verify=False
                response = self.s.post(self.url + endpoint, data=data,
                                       verify=False)  # , verify=False
            else:  # GET
                # response = self.s.get(self.url + endpoint , params=data)  # , verify=False
                response = self.s.get(self.url + endpoint, params=data, verify=False)  # , verify=False

            if response.status_code == 200:
                self.LastResponse = response
                try:
                    self.LastJson = json.loads(response.text)
                    return True
                except:
                    return False
            else:
                print("Request return " + str(response.status_code) + " error!")
                # for debugging
                try:
                    self.LastResponse = response
                    self.LastJson = json.loads(response.text)
                except:
                    pass
                return False
            pass
        except:
            return False
            pass


    def getUserNameInfo(self, userName):
        data = {}
        data['__a'] = 1
        return self.request('{0}/'.format(userName), data)

    def getUserFeed(self, userId, limit = 50, afterId = None):
        data = {}
        data['query_id'] = '17888483320059182'
        if afterId != None:
            data['variables'] = '{"id":"'+str(userId)+'","first":'+str(limit)+',"after":"'+afterId+'"}'
        else:
            data['variables'] = '{"id":"'+str(userId)+'","first":'+str(limit)+'}'
        return self.request('graphql/query/', data)
