import csv
import datetime
import operator
import random
import threading
from functools import reduce
from statistics import mean

import requests
from django.db.models import F, Sum, FloatField, Q, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import dashboard.extDep._tasks.Switches as _switch
from dashboard.models import Output
from . import STRINGS
from .extDep._tasks.Tasks import _thread
from .extDep.insta9.Instagram import instagram
from .extDep.insta9.InstagramWeb import instagramweb
from .extDep.misc.Logs import writeLog
from .models import Brands
from .models import Followers
from .models import Hashtagbrands
from .models import Lists
from .models import Logs
from .models import Post
from .models import Timeseries
from .models import Useraccounts
from .models import Usersinfo


# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'title': "Dashboard"})


def importexport(request):
    return render(request, 'dashboard/importexport.html', {'title': "Import/Export"})


def scrapping(request):
    return render(request, 'dashboard/scrapping.html', {'title': "Scrapping"})


def schedule(request):
    data = {
        'ts': _switch.timeSeries,
        'ui': _switch.usersInfo
    }
    return render(request, 'dashboard/schedule.html', {'title': "Schedule", 'data': data})


def calculations(request):
    return render(request, 'dashboard/calculations.html', {'title': "Calculations"})


def notifications(request):
    return render(request, 'dashboard/notifications.html', {'title': "Notifications"})


def profiles(request):
    return render(request, 'dashboard/profiles.html', {'title': "Profiles"})


def profile(request):
    post = Post.objects.filter(username__exact=request.GET.get("un")).order_by('-post_timestamp')
    data = Usersinfo.objects.get(username__exact=request.GET.get("un"))

    count = (post.aggregate(likes=Sum('likes'), comments=Sum('comments_count'), posts=Count('*')))

    hashTags = Hashtagbrands.objects.order_by('hashtag').filter(
        brands_fk__usersinfo_fk__username__exact=request.GET.get("un"))
    print(hashTags)
    return render(request, 'dashboard/profile.html',
                  {'title': "Profile", "data": data, 'post': post, 'count': count, "hashes": hashTags})


def search(request):
    return render(request, 'dashboard/search.html', {'title': "Search"})


def account(request):
    return render(request, 'dashboard/account.html',
                  {'title': "Account", 'accounts': Useraccounts.objects.order_by("username")[:100]})


# fetch json AJAX

def get_table_count(request):
    data = {
        'usersinfo': len(Usersinfo.objects.all()),
        'brands': Brands.objects.count(),
        # 'followers': Followers.objects.count(),
        'hashtag': Hashtagbrands.objects.count(),
        'post': Post.objects.count(),
        'timeseries': Timeseries.objects.count(),
    }
    return JsonResponse({'data': data})

    # END fetch json AJAX


def accountLogin(request):
    if request.method == 'POST':

        writeLog(1, "Login attempt", STRINGS.login_attempt.format(request.POST.get('un'), request.POST.get('pw')))

        i9 = instagram()
        if i9.login(request.POST.get('un'), request.POST.get('pw')):
            iw = instagramweb()
            iw.getUserNameInfo(i9.LastJson['logged_in_user']['username'])
            data = {
                'username': iw.LastJson['user']['username'],
                'fullname': iw.LastJson['user']['full_name'],
                'bio': iw.LastJson['user']['biography'],
                'profile': iw.LastJson['user']['profile_pic_url'],
            }
            user, created = Useraccounts.objects.update_or_create(username=data['username'])
            user.username = data['username']
            user.password = request.POST.get('pw')
            user.username = data['username']
            user.bio = data['bio']
            user.profilepicture = data['profile']
            user.fullname = data['fullname']
            user.cookie = str(requests.utils.dict_from_cookiejar(i9.s.cookies))
            user.deviceid = i9.device_id
            user.uuid = i9.uuid
            user.advertisingid = i9.advertising_id
            user.phoneid = i9.phone_id
            user.accountid = i9.account_id
            user.save()

            writeLog(4, "Login success", STRINGS.login_success.format(data['username']))

            return JsonResponse({'data': data})
        else:
            try:
                msg = i9.LastJson['message']
            except:
                msg = ''
            writeLog(3, "Login fail", STRINGS.login_fail.format(request.POST.get('un'), request.POST.get('pw'), msg))

    return JsonResponse({'data': ''})


def getLogs(request):
    if request.method == 'POST':
        if request.POST.get('category') != '':
            data = Logs.objects.filter(code__exact=request.POST.get('category'), id__gt=request.POST.get('id')).values(
                'id', 'title', 'code', 'desc',
                'timestamp').order_by(
                'id')[:12]
        else:
            data = Logs.objects.filter(id__gt=request.POST.get('id')).values('id', 'title', 'code', 'desc',
                                                                             'timestamp').order_by('id')[:12]
        return JsonResponse({'data': list(data)})


def scrape(request):
    if request.method == 'POST':
        iw = instagramweb()
        i9 = instagram()
        _accounts = list(Useraccounts.objects.values())
        _i = (random.randint(0, len(_accounts) - 1))

        if iw.getUserNameInfo(request.POST.get('un')) and i9.loadLogin(_accounts[_i]):
            userId = iw.LastJson['user']['id']

            if request.POST.get('category') == 'profile':
                writeLog(1, "Scrapping",
                         STRINGS.scrapping_user.format(request.POST.get('un'), 'Profile', str(datetime.datetime.now())))
                if i9.getInfoById(userId):
                    scrapeUser(i9, iw, userId)
                    return JsonResponse({'data': True})
                pass
            elif request.POST.get('category') == 'feed':
                writeLog(1, "Scrapping",
                         STRINGS.scrapping_user.format(request.POST.get('un'), 'Feed', str(datetime.datetime.now())))
                i9.getTotalUserFeed(userId)
                i9.updateCookies()
                return JsonResponse({'data': True})
                pass
            elif request.POST.get('category') == 'followers':
                writeLog(1, "Scrapping",
                         STRINGS.scrapping_user.format(request.POST.get('un'), 'Followers',
                                                       str(datetime.datetime.now())))

                i9.getTotalFollowers(userId)
                return JsonResponse({'data': True})
                pass
            pass
    return JsonResponse({'data': False})


def massScrape(request):
    if request.method == 'POST':
        iw = instagramweb()
        i9 = instagram()
        _accounts = list(Useraccounts.objects.values())
        _i = (random.randint(0, len(_accounts) - 1))
        if i9.loadLogin(_accounts[_i]):
            if request.POST.get('category') == 'profile':
                writeLog(1, "Scrapping",
                         STRINGS.mass_user.format('Profile', str(datetime.datetime.now())))
                for i in Usersinfo.objects.order_by('username').all():
                    if i9.getInfoById(i.userid):
                        scrapeUser(i9, iw, i.userid)
                return JsonResponse({'data': True})

            elif request.POST.get('category') == 'post':
                writeLog(1, "Scrapping",
                         STRINGS.mass_user.format('Feed', str(datetime.datetime.now())))
                for i in Usersinfo.objects.order_by('username').all():
                    if i9.getTotalUserFeed(i.userid):
                        pass
                return JsonResponse({'data': True})

    return JsonResponse({'data': False})


def _import(request):
    if request.POST and request.FILES:
        try:
            iw = instagramweb()
            i9 = instagram()
            _accounts = list(Useraccounts.objects.values())
            _i = (random.randint(0, len(_accounts) - 1))
            if i9.loadLogin(_accounts[_i]):
                _list = {}
                csvfile = request.FILES['file']
                reader = csv.DictReader(csvfile.read().decode('utf-8').splitlines())
                for r in reader:
                    _list[r['username']] = r['is_brand']

                writeLog(1, "Import",
                         STRINGS.import_users.format(len(_list),
                                                     str(datetime.datetime.now())))

                for i in _list:
                    if iw.getUserNameInfo(i):
                        userId = iw.LastJson['user']['id']
                        if i9.getInfoById(userId):
                            scrapeUser(i9, iw, userId)

                return JsonResponse({'data': True,
                                     'count': len(_list), })
        except Exception as e:
            return JsonResponse({'data': False,
                                 'msg': str(e)})

    return JsonResponse({'data': False})


def _export(request):
    if request.method == 'GET':

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(request.GET.get('name'))

        fieldnames = ['username', 'is_brand']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()

        for u in Usersinfo.objects.annotate(b_id=F('brand2usersinfo__brands_fk__usersinfo_fk_id')).values('id',
                                                                                                          'username',
                                                                                                          'b_id').order_by(
            'username').all():
            writer.writerow({'username': u['username'], 'is_brand': 1 if u['b_id'] else 0})

        return response

    return JsonResponse({'data': False})


def getProfiles(request):
    MAXLIMIT = 23

    if request.method == 'POST':

        descending = request.POST.get("order") == 'desc'

        _range = request.POST.get("range").split(';')

        kwargs = {}
        if request.POST.get("private") == 'true' and request.POST.get("public") == 'true':
            pass
        elif request.POST.get("public") == 'true':
            kwargs['isprivate'] = False
        elif request.POST.get("private") == 'true':
            kwargs['isprivate'] = True
        else:
            pass

        if len(_range) > 1:
            if int(_range[1]) >= 3000000:
                kwargs['followed_by__gte'] = int(_range[0])
            else:
                kwargs['followed_by__gte'] = int(_range[0])
                kwargs['followed_by__lte'] = int(_range[1])
        else:
            kwargs['followed_by__gte'] = int(0)





        if request.POST.get("sort"):

            if request.POST.get("sort") == 'sort2':
                if descending:
                    order = '-post_timestamp'
                    if request.POST.get("lastactive"):
                        kwargs['post_timestamp__lt'] = request.POST.get('lastactive')
                else:
                    order = 'post_timestamp'
                    if request.POST.get("lastactive"):
                        kwargs['post_timestamp__gt'] = request.POST.get('lastactive')

            elif request.POST.get("sort") == 'sort3':
                if descending:
                    order = '-followed_by'
                    if request.POST.get("followers"):
                        kwargs['followed_by__lt'] = request.POST.get('followers')
                else:
                    order = 'followed_by'
                    if request.POST.get("followers"):
                        kwargs['followed_by__gt'] = request.POST.get('followers')

            elif request.POST.get("sort") == 'sort4':
                if descending:
                    order = '-engagement'
                    if request.POST.get("engagement"):
                        kwargs['engagement__lt'] = request.POST.get('engagement')
                else:
                    order = 'engagement'
                    if request.POST.get("engagement"):
                        kwargs['engagement__gt'] = request.POST.get('engagement')

            else:
                if descending:
                    order = '-username'
                    if request.POST.get("lastuser"):
                        kwargs['username__lt'] = request.POST.get('lastuser')
                else:
                    order = 'username'
                    if request.POST.get("lastuser"):
                        kwargs['username__gt'] = request.POST.get('lastuser')

        if request.POST.get("list") == '_all':
            pass
        else:
            kwargs['username__in'] = Lists.objects.get(name=request.POST.get("list")).items.split(",")
            print(kwargs['username__in'])
            pass

        if request.POST.get("brands") == 'false':
            data = Usersinfo.objects.order_by(order).values('username', 'userid', 'fullname', 'bio', 'isprivate',
                                                            'followed_by', 'follows', 'profilepicture',
                                                            'media_count', 'is_verified', 'is_business',
                                                            'comments_count',
                                                            'likes_count', 'website', 'email').annotate(
                engagement=Sum(F('likes_count') / F('followed_by') * 100, output_field=FloatField()),
                row_id=F('id')).filter(**kwargs)[
                   :MAXLIMIT]
            print(data)

        else:
            data = Brands.objects.order_by(order).values('id').annotate(row_id=F('usersinfo_fk__username'),
                                                                        username=F('usersinfo_fk__username'),
                                                                        userid=F('usersinfo_fk__userid'),
                                                                        fullname=F('usersinfo_fk__fullname'),
                                                                        bio=F('usersinfo_fk__bio'),
                                                                        isprivate=F('usersinfo_fk__isprivate'),
                                                                        followed_by=F('usersinfo_fk__followed_by'),
                                                                        follows=F('usersinfo_fk__follows'),
                                                                        profilepicture=F(
                                                                            'usersinfo_fk__profilepicture'),
                                                                        media_count=F('usersinfo_fk__media_count'),
                                                                        is_verified=F('usersinfo_fk__is_verified'),
                                                                        is_business=F('usersinfo_fk__is_business'),
                                                                        comments_count=F(
                                                                            'usersinfo_fk__comments_count'),
                                                                        likes_count=F('usersinfo_fk__likes_count'),
                                                                        website=F('usersinfo_fk__website'),
                                                                        email=F('usersinfo_fk__email'),
                                                                        engagement=Sum(
                                                                            F('likes_count') / F('followed_by') * 100,
                                                                            output_field=FloatField())).filter(
                **kwargs)[:MAXLIMIT]


        return JsonResponse({'data': list(data)})


def getProfile(request):
    if request.method == 'POST':
        data = Usersinfo.objects.values('username', 'userid', 'fullname', 'bio', 'isprivate',
                                        'followed_by', 'follows', 'profilepicture',
                                        'media_count', 'is_verified', 'is_business', 'comments_count',
                                        'likes_count', 'website', 'email').annotate(
            engagement=Sum(F('likes_count') / F('followed_by') * 100, output_field=FloatField()),
            row_id=F('id')).filter(
            username__exact=request.POST.get('un'))[:1]

        return JsonResponse({'data': list(data)})


def getSuggestions(request):
    if request.method == 'GET':
        if request.GET.get('query'):
            if request.GET.get('cat') == 'followers':
                followers = Followers.objects.values('username').filter(username__startswith=request.GET.get('query'))[
                            :5]
                return JsonResponse({'fn': list(followers)})
            else:
                userNames = Usersinfo.objects.values('username', 'fullname').filter(
                    Q(username__istartswith=request.GET.get('query')) | Q(
                        fullname__istartswith=request.GET.get('query')))[:5]
                # hashTags = Hashtagbrands.objects.values('hashtag', 'brands_fk__usersinfo_fk__username')[:5]
                return JsonResponse({'un': list(userNames)})

    return JsonResponse()

    pass


def _schedule(request):
    if request.method == 'POST':
        t = _thread()
        threading.Thread(target=t.init, args=()).start()
        _event = request.POST.get('event')
        if request.POST.get('cat') == 'ts':
            if _event == 'start':
                t.scheduleTS()
                # _switch.timeSeries.start()
                return JsonResponse({'data': True})
                pass
            elif _event == 'pause':
                _switch.timeSeries.pause()
                return JsonResponse({'data': True})
                pass
            elif _event == 'resume':
                _switch.timeSeries.resume()
                return JsonResponse({'data': True})
                pass
            elif _event == 'stop':
                _switch.timeSeries.stop()
                return JsonResponse({'data': True})
                pass
            pass
        elif request.POST.get('cat') == 'ui':
            if _event == 'start':
                t.scheduleUI()
                # _switch.usersInfo.start()
                return JsonResponse({'data': True})
                pass
            elif _event == 'pause':
                _switch.usersInfo.pause()
                return JsonResponse({'data': True})
                pass
            elif _event == 'resume':
                _switch.usersInfo.resume()
                return JsonResponse({'data': True})
                pass
            elif _event == 'stop':
                _switch.usersInfo.stop()
                return JsonResponse({'data': True})
                pass
            pass

    return JsonResponse({})


def createList(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            _list, created = Lists.objects.get_or_create(name=request.POST.get('list'))
            if created:
                _list.items = request.POST.get('values')
                _list.save()
                return JsonResponse({'status': 'created'})
            else:
                _list.items = request.POST.get('values')
                _list.save()
                return JsonResponse({'status': 'updated'})
            pass
        elif request.POST.get('action') == 'del':
            try:
                _list = Lists.objects.get(name=request.POST.get('list'))
                _list.delete()
                return JsonResponse({'status': 'deleted'})
            except:
                return JsonResponse({'status': 'notfound'})
                pass

        elif request.POST.get('action') == 'load':
            data = Lists.objects.order_by('name').values('name', 'items')[:1000]

            return JsonResponse({'status': 'load', 'data': list(data)})
            pass
        elif request.POST.get('action') == 'loadprofiles':
            _l = Lists.objects.get(name=request.POST.get('ln'))

            data = Usersinfo.objects.values('username', 'userid', 'fullname', 'bio', 'isprivate',
                                            'followed_by', 'follows', 'profilepicture',
                                            'media_count', 'is_verified', 'comments_count',
                                            'likes_count', 'website', 'email').annotate(
                engagement=Sum(F('likes_count') / F('followed_by') * 100, output_field=FloatField()),
                row_id=F('id')).filter(
                username__in=_l.items.split(','))
            return JsonResponse({'status': 'load', 'data': list(data), 'ln': _l.name})
            pass

    return JsonResponse({})


def getStats(request):
    if request.method == 'GET':
        row_id = int(request.GET.get('row_id'))
        duration = int(request.GET.get("duration"))
        data = Timeseries.objects.values('timestamp', 'followed_by', 'likes_count', 'comments_count').filter(
            usesinfoid_fk_id=row_id).order_by('timestamp')[:duration]
        return JsonResponse({'data': list(data)})
        pass
    pass


def output(request):
    if request.method == "GET":
        kwargs = {'oid': request.GET.get('oid'), 'id__gt': request.GET.get('lid')}

        data = Output.objects.order_by('-timestamp').values('id', 'message', 'timestamp').filter(**kwargs)[:10]
        return JsonResponse({'data': list(reversed(data))})

        pass


def lists(request):
    if request.GET.get('action') == 'load':
        if request.GET.get('sub_action') == 'save':
            _data = Lists.objects.order_by('name').values('name', 'items').all()
            return JsonResponse({'data': list(_data)})
        elif request.GET.get('sub_action') == 'del':
            _list = request.GET.get('items').split(',')

            query = reduce(operator.or_, (Q(items__iregex='[[:<:]]{0}[[:>:]]'.format(item)) for item in _list))

            _data = Lists.objects.order_by('name').values('name', 'items').filter(query).all()
            return JsonResponse({'data': list(_data)})

    elif request.GET.get('action') == 'save':
        _list = request.GET.get('items').split(',')
        _data, created = Lists.objects.get_or_create(name=request.GET.get('name'))
        if created:
            _data.items = ",".join(list(set(_list)))
            _data.save()
            return JsonResponse({'data': 'created'})
        _list.extend(_data.items.split(',')) if _data.items else None
        _data.items = ','.join(list(set(_list)))
        _data.save()
        return JsonResponse({'data': 'updated'})


    elif request.GET.get('action') == 'del':
        _list = request.GET.get('items').split(',')
        _data, created = Lists.objects.get_or_create(name=request.GET.get('name'))
        if created:
            return JsonResponse({'data': 'created'})
        _l = _data.items.split(',')
        for i in _list:
            _l.remove(i)
            pass
        _data.items = ','.join(list(set(_l)))
        _data.save()
        return JsonResponse({'data': 'deleted'})

    elif request.GET.get('action') == 'create':
        _data, created = Lists.objects.get_or_create(name=request.GET.get('name'))
        if created:
            _data.save()
            return JsonResponse({'data': 'created'})
        return JsonResponse({'data': 'exist'})

    return JsonResponse({'data': False})


def temp(request):
    _arg = request.GET.get('arg')

    # data = Post.objects.values('username').annotate(Count('username'), timestamp=Max('timestamp')).order_by(
    #     '-timestamp').all()

    currentDay = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    data = Usersinfo.objects.values('id', 'userid', 'username', 'followed_by').filter(
        ~Q(timeseries__timestamp__gt=currentDay), isprivate=0).order_by('-followed_by').all()

    return JsonResponse({'data': list(data)})


def profilesQuery(request):
    if request.method == 'POST':
        if request.POST.get("cat") == 'user':
            userNames = Usersinfo.objects.values('username', 'fullname', 'profilepicture').filter(
                Q(username__istartswith=request.POST.get('query')) | Q(
                    fullname__istartswith=request.POST.get('query')))[:5]
            return JsonResponse({'users': list(userNames)})
        else:
            userNames = Hashtagbrands.objects.annotate(username=F('brands_fk__usersinfo_fk__username'),
                                                       fullname=F('brands_fk__usersinfo_fk__fullname'),
                                                       profilepicture=F(
                                                           'brands_fk__usersinfo_fk__profilepicture')).values(
                'username', 'fullname', 'profilepicture', 'hashtag').filter(
                Q(hashtag__startswith=request.POST.get('query')))[:5]

            return JsonResponse({'hash': list(userNames)})

    pass

# Extra functions

def scrapeUser(i9, iw, userId):
    try:
        u, created = Usersinfo.objects.get_or_create(userid=userId)
        u.username = i9.LastJson['user']['username']
        u.userid = i9.LastJson['user']['pk']
        u.fullname = i9.LastJson['user']['full_name']
        u.bio = i9.LastJson['user']['biography']
        u.isprivate = i9.LastJson['user']['is_private']
        u.followed_by = i9.LastJson['user']['follower_count']
        u.follows = i9.LastJson['user']['following_count']
        u.profilepicture = i9.LastJson['user']['profile_pic_url']

        try:
            u.geo_media_count = i9.LastJson['user']['geo_media_count']
        except:
            pass
        try:
            u.media_count = i9.LastJson['user']['media_count']
        except:
            pass
        try:
            u.usertags_count = i9.LastJson['user']['usertags_count']
        except:
            pass
        try:
            u.is_verified = i9.LastJson['user']['is_verified']
        except:
            pass
        try:
            u.is_business = i9.LastJson['user']['is_business']
        except:
            pass
        try:
            u.website = i9.LastJson['user']['external_url']
        except:
            pass
        try:
            u.email = i9.LastJson['user']['public_email']
        except:
            pass
        pass

        if iw.getUserFeed(userId):

            _likes = []
            _comments = []
            for n in iw.LastJson['data']['user']['edge_owner_to_timeline_media']['edges']:
                _likes.append(n['node']['edge_media_to_comment']['count'])
                _comments.append(n['node']['edge_media_preview_like']['count'])
            pass

            try:
                u.comments_count = mean(_likes)
            except:
                pass
            try:
                u.likes_count = mean(_comments)
            except:
                pass
        u.save()
        return True
    except:
        return False
