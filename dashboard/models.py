from __future__ import unicode_literals

from django.db import models


class Brand2Usersinfo(models.Model):
    usersinfo_fk = models.ForeignKey('Usersinfo', models.DO_NOTHING, db_column='usersinfo_fk')
    brands_fk = models.ForeignKey('Brands', models.DO_NOTHING, db_column='brands_fk')
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'brand2usersinfo'


class Brands(models.Model):
    usersinfo_fk = models.ForeignKey('Usersinfo', models.DO_NOTHING, db_column='usersinfo_fk')
    # usersinfo_fk = models.ForeignKey('Usersinfo', models.DO_NOTHING, db_column='usersinfo_fk', unique=True)
    name = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Followers(models.Model):
    username = models.CharField(max_length=99, blank=True, null=True)
    userid = models.BigIntegerField(db_column='userID', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        managed = False
        db_table = 'followers'


class Followers2Usersinfo(models.Model):
    usersinfo_fk = models.ForeignKey('Usersinfo', models.DO_NOTHING, db_column='usersinfo_fk', blank=True, null=True)
    followers_fk = models.ForeignKey(Followers, models.DO_NOTHING, db_column='followers_fk', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        managed = False
        db_table = 'followers2usersinfo'
        unique_together = (('usersinfo_fk', 'followers_fk'),)


class Hashtagbrands(models.Model):
    hashtag = models.CharField(max_length=99, blank=True, null=True)
    brands_fk = models.ForeignKey(Brands, models.DO_NOTHING, db_column='brands_fk', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hashtagBrands'
        unique_together = (('hashtag', 'brands_fk'),)


class Hashtagstyle(models.Model):
    hashtag = models.CharField(max_length=99, blank=True, null=True)
    firstviewtimestamp = models.DateTimeField(db_column='firstviewTimestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hashtagStyle'


class Post(models.Model):
    postid = models.CharField(db_column='postID', unique=True, max_length=200)  # Field name made lowercase.
    post_timestamp = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=99, blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    comment_likes_count = models.IntegerField(blank=True, null=True)
    postpicture = models.TextField(db_column='postPicture', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'post'


class Style2Hashtag(models.Model):
    hashtagstyle_fk = models.ForeignKey(Hashtagstyle, models.DO_NOTHING, db_column='hashtagStyle_fk', blank=True,
                                        null=True)  # Field name made lowercase.
    styles_fk = models.ForeignKey('Styles', models.DO_NOTHING, db_column='styles_fk', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'style2hashtag'
        unique_together = (('hashtagstyle_fk', 'styles_fk'),)


class Styles(models.Model):
    name = models.CharField(max_length=99, blank=True, null=True)
    description = models.CharField(max_length=99, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'styles'


class Timeseries(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    usesinfoid_fk = models.ForeignKey('Usersinfo', models.DO_NOTHING, db_column='usesinfoID_fk', blank=True,
                                      null=True)  # Field name made lowercase.
    likes_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    followed_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timeseries'


class Usersinfo(models.Model):
    username = models.CharField(unique=True, max_length=99)
    userid = models.BigIntegerField(db_column='userID', unique=True)  # Field name made lowercase.
    fullname = models.CharField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    isprivate = models.IntegerField(db_column='isPrivate', blank=True, null=True)  # Field name made lowercase.
    followed_by = models.BigIntegerField(blank=True, null=True)
    follows = models.IntegerField(blank=True, null=True)
    profilepicture = models.TextField(db_column='profilePicture', blank=True, null=True)  # Field name made lowercase.
    geo_media_count = models.IntegerField(blank=True, null=True)
    media_count = models.IntegerField(blank=True, null=True)
    usertags_count = models.IntegerField(blank=True, null=True)
    is_verified = models.IntegerField(blank=True, null=True)
    is_business = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    likes_count = models.IntegerField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'usersinfo'


# Extra

class Useraccounts(models.Model):
    fullname = models.CharField(max_length=500, blank=True, null=True)
    username = models.CharField(unique=True, max_length=99)
    password = models.CharField(max_length=200)
    profilepicture = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    cookie = models.TextField(blank=True, null=True)
    deviceid = models.CharField(max_length=99, null=True)
    uuid = models.CharField(max_length=199, null=True)
    advertisingid = models.CharField(max_length=199, null=True)
    phoneid = models.CharField(max_length=199, null=True)
    accountid = models.CharField(max_length=99, null=True)
    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'useraccounts'


class Logs(models.Model):
    code = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'logs'


class Tasks(models.Model):
    threadid = models.BigIntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=99, blank=True, null=True)
    input = models.TextField(blank=True, null=True)
    stop = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tasks'


class Lists(models.Model):
    name = models.CharField(unique=True, max_length=99, blank=True, null=True)
    items = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lists'


class Output(models.Model):
    oid = models.IntegerField(blank=True, null=True)
    # 1 = TimeSeries Scheduling
    # 2 = UsersInfo Scheduling
    # 3 = UsersInfo single
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'output'
