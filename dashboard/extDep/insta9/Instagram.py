import ast
import hashlib
import hmac
import json
import re
import time
import urllib
import uuid

import requests

from dashboard.models import Followers, Followers2Usersinfo, Usersinfo, Post, Useraccounts
from .CONSTANTS import const


class instagram:
    ##global variables
    # username
    # password
    # device
    # uuid
    # advertising_id
    # device_id
    # phone_id
    # account_id
    # isLoggedIn
    # rank_token
    # session_id
    # experiments

    DEVICE_SETTINTS = {
        'manufacturer': 'Xiaomi',
        'model': 'HM 1SW',
        'chip': 'armani',
        'version': const.IG_VERSION
    }

    USER_AGENT = 'Instagram {version} Android (18/4.3; 320dpi; 720x1280; {manufacturer}; {model}; {chip}; qcom; en_US)'.format(
        **DEVICE_SETTINTS)

    def login(self, username, password, forced=False):
        self.s = requests.Session()
        self._setUser(username, password)

        self._sendPreLoginFlow()

        data = {}
        data['phone_id'] = self.phone_id
        data['_csrftoken'] = self.getToken()
        data['username'] = self.username
        data['adid'] = self.advertising_id
        data['guid'] = self.uuid
        data['device_id'] = self.device_id
        data['password'] = self.password
        data['login_attempt_count'] = 0

        if self.request('accounts/login/', self.generateSignature(data), True):
            try:
                if self.LastJson['status'] == 'ok':
                    self.account_id = self.LastJson['logged_in_user']['pk']
                    return True
            except:
                pass
            pass
        return False
        pass

    def loadLogin(self, account, forced=False):
        self.s = requests.Session()

        self.username = account['username']
        self.password = account['password']
        self.uuid = account['uuid']
        self.device_id = account['deviceid']
        self.advertising_id = account['advertisingid']
        self.phone_id = account['phoneid']
        self.account_id = account['accountid']
        self.rank_token = self.generateUUID(True)
        self.s.cookies = requests.utils.cookiejar_from_dict(ast.literal_eval(account['cookie']))
        return self.syncDeviceFeatures()

        pass

    def getInfoById(self, userId):
        data = {}
        data['device_id'] = self.device_id

        return self.request("users/{0}/info/".format(userId), data)

    def getFollowers(self, userId, maxId=None, searchQuery=None):
        data = {}
        data['rank_token'] = self.rank_token
        if maxId != None:
            data['max_id'] = maxId
        if searchQuery != None:
            data['query'] = searchQuery

        return self.request("friendships/{0}/followers/".format(userId), data)

    def getTotalFollowers(self, userId, modelToStoreDB=None):
        try:
            next_mid = None
            while True:
                if self.getFollowers(userId, next_mid):
                    for user in self.LastJson['users']:
                        try:
                            f, created = Followers.objects.update_or_create(username=user['username'])
                            f.username = user['username']
                            f.userid = user['pk']
                            if created:
                                f.save()
                            f2, created2 = Followers2Usersinfo.objects.update_or_create(
                                usersinfo_fk_id=list(Usersinfo.objects.values('id').filter(userid=int(userId))[:1])[0][
                                    'id'],
                                followers_fk_id=f.id)
                            f2.usersinfo_fk_id = list(Usersinfo.objects.values('id').filter(userid=int(userId))[:1])[0][
                                'id']
                            f2.followers_fk_id = f.id

                            f2.save()
                        except:
                            pass

                    if self.LastJson['next_max_id'] is not None:
                        next_mid = self.LastJson['next_max_id']
                        time.sleep(7)
                    else:
                        break
        except:
            pass

    def getUserFeed(self, usernameId, maxid=None, minTimestamp=None):

        data = {}
        if maxid != None:
            data['max_id'] = str(maxid)
        if minTimestamp != None:
            data['min_timestamp'] = str(minTimestamp)
        data['rank_token'] = self.rank_token
        data['ranked_content'] = True

        return self.request('feed/user/{0}/'.format(usernameId), data)

    def getTotalUserFeed(self, userId):
        user_feed = []
        next_max_id = None
        _c = []
        _l = []
        while True:
            if self.getUserFeed(userId, next_max_id):
                temp = self.LastJson
                for item in temp["items"]:
                    user_feed.append(1)
                    _l.append(item['like_count'])
                    _c.append(item['comment_count'])

                    p, p_created = Post.objects.update_or_create(postid=item['id'])
                    try:
                        p.postid = item['id']
                    except:
                        pass
                    try:
                        p.post_timestamp = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(item['taken_at']))
                    except:
                        pass
                    try:
                        p.username = item['user']['username']
                    except:
                        pass
                    try:
                        p.likes = item['like_count']
                    except:
                        pass
                    try:
                        p.comments_count = item['comment_count']
                    except:
                        pass
                    try:
                        p.caption = item['caption']['text']
                    except:
                        pass
                    try:
                        p.location = "{0},{1}".format(item['lat'], item['lng'])
                    except:
                        pass
                    try:
                        p.tags = ",".join(re.findall(r'(?<=#)(\w*[A-Za-z_]+\w*)', item['caption']['text'], re.I))
                    except:
                        pass
                    try:
                        p.comment_likes_count = 0
                    except:
                        pass
                    try:
                        p.postpicture = item['image_versions2']['candidates'][0]['url']
                    except:
                        pass
                    p.save()

                    if len(user_feed) > 49:
                        return True
                if not temp["more_available"]:
                    return True
                next_max_id = temp["next_max_id"]

            else:
                return False

    def _setUser(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.advertising_id = self.generateUUID(True)
        self.phone_id = self.generateUUID(True)

        self.isLoggedIn = False

        pass

    def getToken(self):
        try:
            return self.LastResponse.cookies['csrftoken']
        except:
            return requests.utils.dict_from_cookiejar(self.s.cookies)['csrftoken']
        pass

    def request(self, endpoint, data=None, post=False):
        # if (not self.isLoggedIn):
        #     raise Exception("Not logged in!\n")
        #     return

        self.s.headers.update({'Connection': 'close',
                               'Accept': '*/*',
                               'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'Accept-Language': 'en-US',
                               'User-Agent': self.USER_AGENT})

        if (post):  # POST
            # response = self.s.post(const.API_URLS[1] + endpoint, data=post)  # , verify=False
            response = self.s.post(const.API_URLS[1] + endpoint, data=data,
                                   verify=False)  # , verify=False
        else:  # GET
            # response = self.s.get(const.API_URLS[1] + endpoint , params=data)  # , verify=False
            response = self.s.get(const.API_URLS[1] + endpoint, params=data, verify=False)  # , verify=False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
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

    def _sendPreLoginFlow(self):
        self.syncDeviceFeatures(True)
        self.readMsisdnHeader()
        self.logAttribution()

    def syncDeviceFeatures(self, prelogin=False):
        data = {}
        data['id'] = self.uuid
        data['experiments'] = const.LOGIN_EXPERIMENTS
        if prelogin:
            return self.request('qe/sync/', self.generateSignature(data), True)
        data['_uuid'] = self.uuid
        data['_uid'] = self.account_id
        data['_csrftoken'] = self.getToken()

        return self.request('qe/sync/', self.generateSignature(data), True)

    def readMsisdnHeader(self, subnoKey=None):
        data = {}
        data['device_id'] = self.uuid
        data['_csrftoken'] = self.getToken()
        if subnoKey != None:
            data['subno_key'] = subnoKey

        self.request("accounts/read_msisdn_header/", self.generateSignature(data), True)

    def logAttribution(self):
        data = {}
        data['adid'] = self.advertising_id
        self.request('attribution/log_attribution/', self.generateSignature(data), True)

    def generateSignature(self, data):
        data = json.dumps(data)
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

        return 'ig_sig_key_version=' + const.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
            const.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateUUID(self, type):
        # according to https://github.com/LevPasha/Instagram-API-python/pull/16/files#r77118894
        # uuid = '%04x%04x-%04x-%04x-%04x-%04x%04x%04x' % (random.randint(0, 0xffff),
        #    random.randint(0, 0xffff), random.randint(0, 0xffff),
        #    random.randint(0, 0x0fff) | 0x4000,
        #    random.randint(0, 0x3fff) | 0x8000,
        #    random.randint(0, 0xffff), random.randint(0, 0xffff),
        #    random.randint(0, 0xffff))
        generated_uuid = str(uuid.uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def updateCookies(self):
        if self.syncDeviceFeatures():
            user = Useraccounts.objects.get(accountid=self.account_id)

            user.cookie = str(requests.utils.dict_from_cookiejar(self.s.cookies))

            user.save()
