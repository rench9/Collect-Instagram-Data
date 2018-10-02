import datetime
import random
import threading
import time
from statistics import mean

import schedule
from django.db.models import Q

import dashboard.extDep._tasks.Switches as _switch
from dashboard.extDep.misc.Logs import writeLog
from dashboard.models import Usersinfo, Timeseries, Useraccounts, Output
from ..insta9.Instagram import instagram
from ..insta9.InstagramWeb import instagramweb

TIME = "12:17"

class _thread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(_thread, self).__init__()

    def init(self):
        if not _switch.main.started():
            print("init")
            _switch.main.start()
            t1 = threading.Thread(target=self.runPending(), args=())
            t1.start()
        else:
            pass
        pass

    def runPending(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    # def scheduleTS(self):
    #     s1 = sched.scheduler(time.time, time.sleep)
    #
    #     while True:
    #         if _switch.timeSeries.started():
    #             s1.enter(self.everyDayAt("00:30"), 1, self._scrapeTimeseriesPost, argument=())
    #             s1.run()
    #
    #             #     while _switch.timeSeries.started():
    #             #         if not _switch.timeSeries.started():
    #             #             break
    #             #         schedule.run_pending()
    #             #         time.sleep(2)
    #             # time.sleep(2)
    #
    # def scheduleUI(self):
    #     s = sched.scheduler(time.time, time.sleep)
    #
    #     while True:
    #         if _switch.usersInfo.started():
    #             s.enter(self.everyMondayAt("15:30"), 1, self._scrapeUsersInfo, argument=())
    #             s.run()

    def scheduleTS(self):
        if not _switch.timeSeries.started():
            _switch.timeSeries.start()

            schedule.every().day.at("00:30").do(self._scrapeTimeseriesPost)
            schedule.every().day.at("12:30").do(self._scrapeTimeseriesPost)
            # schedule.every().day.at(TIME).do(self._scrapeTimeseriesPost)
            # schedule.every().minute.do(self._scrapeTimeseriesPost)


    def scheduleUI(self):
        if not _switch.usersInfo.started():
            _switch.usersInfo.start()

            schedule.every().friday.at("06:30").do(self._scrapeUsersInfo)
            # schedule.every().day.at(TIME).do(self._scrapeUsersInfo)
            # schedule.every().minute.do(self._scrapeUsersInfo)


    # def scheduleTS(self):
    #
    #     # self.start('Schedule Timeseries')
    #     # schedule.every().day.at("00:30").do(self._scrapeTimeseriesPost)
    #     schedule.every().day.at(TIME).do(self._scrapeTimeseriesPost)
    #     # schedule.every().second.do(self._scrapeTimeseriesPost)
    #
    #     while True:
    #         if _switch.timeSeries.started():
    #
    #             while _switch.timeSeries.started():
    #                 if not _switch.timeSeries.started():
    #                     break
    #                 schedule.run_pending()
    #                 time.sleep(2)
    #         time.sleep(2)
    #
    #         # schedule.every().second.do(self._scrapeTimeseriesPost)
    #         # while not self.stopped():
    #         #     if _switch.timeSeries == 0:
    #         #         self.stop()
    #         #         break
    #         #     schedule.run_pending()
    #         #     time.sleep(2)
    #
    # def scheduleUI(self):
    #     # self.start('Schedule Usersinfo')
    #
    #     while True:
    #         if _switch.usersInfo.started():
    #             # schedule.every().wednesday.at("15:30").do(self._scrapeUsersInfo)
    #             schedule.every().day.at(TIME).do(self._scrapeUsersInfo)
    #             # schedule.every().second.do(self._scrapeUsersInfo)
    #             while _switch.usersInfo.started():
    #                 if not _switch.usersInfo.started():
    #                     break
    #                 schedule.run_pending()
    #                 time.sleep(2)
    #         time.sleep(2)
    #
    #         # schedule.every().monday.at("15:30").do(self._scrapeUsersInfo)
    #         # # schedule.every().second.do(self._scrapeUsersInfo)
    #         # while not self.stopped():
    #         #     if not _switch.usersInfo.started():
    #         #         self.stop()
    #         #         break
    #         #     schedule.run_pending()
    #         #     time.sleep(2)

    def _scrapeUsersInfo(self):
        i9 = instagram()
        iw = instagramweb()
        _accounts = list(Useraccounts.objects.values())
        _i = (random.randint(0, len(_accounts) - 1))
        i9.loadLogin(_accounts[_i])
        for u in Usersinfo.objects.order_by('username').values('id', 'userid', 'username'):
            print("UI" + u['username'])
            self.output(2, 'Scraping {0}'.format(u['username']))
            if _switch.usersInfo.paused():
                while _switch.usersInfo.paused():
                    time.sleep(1)
                pass
            if not _switch.usersInfo.started():
                break
            # continue
            try:
                if i9.getInfoById(u['userid']):
                    user, created = Usersinfo.objects.get_or_create(userid=u['userid'])
                    user.username = i9.LastJson['user']['username']
                    user.userid = i9.LastJson['user']['pk']
                    user.fullname = i9.LastJson['user']['full_name']
                    # user.bio = i9.LastJson['user']['biography']
                    user.isprivate = i9.LastJson['user']['is_private']
                    user.followed_by = i9.LastJson['user']['follower_count']
                    user.follows = i9.LastJson['user']['following_count']
                    user.profilepicture = i9.LastJson['user']['profile_pic_url']

                    try:
                        user.geo_media_count = i9.LastJson['user']['geo_media_count']
                    except:
                        pass
                    try:
                        user.media_count = i9.LastJson['user']['media_count']
                    except:
                        pass
                    try:
                        user.usertags_count = i9.LastJson['user']['usertags_count']
                    except:
                        pass
                    try:
                        user.is_verified = i9.LastJson['user']['is_verified']
                    except:
                        pass
                    try:
                        user.is_business = i9.LastJson['user']['is_business']
                    except:
                        pass
                    try:
                        user.website = i9.LastJson['user']['external_url']
                    except:
                        pass
                    try:
                        user.email = i9.LastJson['user']['public_email']
                    except:
                        pass

                    if iw.getUserFeed(u['userid']):

                        _likes = []
                        _comments = []
                        for n in iw.LastJson['data']['user']['edge_owner_to_timeline_media']['edges']:
                            _likes.append(n['node']['edge_media_to_comment']['count'])
                            _comments.append(n['node']['edge_media_preview_like']['count'])
                        pass

                        try:
                            user.comments_count = mean(_likes)
                        except:
                            pass
                        try:
                            user.likes_count = mean(_comments)
                        except:
                            pass

                    if not user.isprivate:
                        try:
                            i9.getTotalUserFeed(u['userid'])
                        except:
                            pass
                    user.save()
            except Exception as E:
                writeLog(3, "UsersInfo Exception", str(E))
                pass
            time.sleep(random.randint(5, 12))

    def _scrapeTimeseriesPost(self):
        iw = instagramweb()

        currentDay = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # for u in Usersinfo.objects.order_by('-followed_by').filter(isprivate=0).values('id', 'userid',
        #                                                                     'username',
        #                                                                     'followed_by'):
        for u in Usersinfo.objects.values('id', 'userid', 'username', 'followed_by').filter(
                ~Q(timeseries__timestamp__gt=currentDay), isprivate=0).order_by('-followed_by').all():
            print(u['username'])

            if _switch.timeSeries.paused():
                while _switch.timeSeries.paused():
                    time.sleep(1)
                pass
            if not _switch.timeSeries.started():
                break
            # continue
            try:
                if iw.getUserNameInfo(u['username']):
                    self.output(1, 'Scraping {0}'.format(u['username']))
                    t = Timeseries.objects.create()
                    t.usesinfoid_fk_id = u['id']
                    t.followed_by = iw.LastJson['user']['followed_by']['count']
                    if iw.getUserFeed(u['userid']):
                        _c = []
                        _l = []
                        for p in iw.LastJson['data']['user']['edge_owner_to_timeline_media']['edges']:
                            _c.append(p['node']['edge_media_to_comment']['count'])
                            _l.append(p['node']['edge_media_preview_like']['count'])
                            pass
                        try:
                            t.likes_count = sum(_l)
                        except:
                            pass
                        try:
                            t.comments_count = sum(_c)
                        except:
                            pass

                        pass

                    t.save()

                    pass
                pass
            except Exception as E:
                writeLog(3, "Timeseries Exception", str(E))
                pass

            time.sleep(random.randint(5, 12))

    def output(self, code, message):
        output = Output.objects.create()
        output.oid = code
        output.message = message
        output.save()

        # def everyDayAt(self, hourTime):
        #     _format = "%H:%M"
        #     _hourTime = datetime.datetime.strptime(hourTime, _format)
        #     _ct = datetime.datetime.now()
        #     _dt = datetime.datetime.now().replace(hour=_hourTime.hour, minute=_hourTime.minute)
        #
        #     if _ct >= _dt:
        #         _ct += datetime.timedelta(days=1)
        #         return _ct.timestamp() - _dt.timestamp()
        #     return _dt.timestamp() - _ct.timestamp()
        #
        # def everyMondayAt(self, hourTime):
        #     _format = "%H:%M"
        #     _hourTime = datetime.datetime.strptime(hourTime, _format)
        #     _ct = datetime.datetime.now()
        #     _dt = datetime.datetime.now().replace(hour=_hourTime.hour, minute=_hourTime.minute)
        #
        #     if _ct >= _dt:
        #         _dt = _dt + datetime.timedelta(days=(8 - _ct.isoweekday()))
        #
        #         print(_dt.timestamp(), _ct.timestamp())
        #         return _dt.timestamp() - _ct.timestamp()
        #
        #     print(_dt.timestamp(), _ct.timestamp())
        #     return _dt.timestamp() - _ct.timestamp()
