from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^importexport$', views.importexport, name='importexport'),
    url(r'^scrapping$', views.scrapping, name='scrapping'),
    url(r'^schedule$', views.schedule, name='schedule'),
    url(r'^calculation$', views.calculations, name='calculations'),
    url(r'^notifications$', views.notifications, name='notifications'),
    url(r'^profiles$', views.profiles, name='profiles'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^search$', views.search, name='search'),
    url(r'^account$', views.account, name='account'),
    url(r'^get/tablecount$', views.get_table_count, name='tablecount'),
    url(r'^post/accountslogin$', views.accountLogin, name='accountlogin'),
    url(r'^post/logs$', views.getLogs, name='logs'),
    url(r'^post/scrape$', views.scrape, name='scrape'),
    url(r'^post/massscrape$', views.massScrape, name='massscrape'),
    url(r'^post/import$', views._import, name='_import'),
    url(r'^post/export$', views._export, name='export'),
    url(r'^post/profiles$', views.getProfiles, name='getprofiles'),
    url(r'^post/profiles/search$', views.profilesQuery, name='getprofiles'),
    url(r'^post/profile$', views.getProfile, name='getprofile'),
    url(r'^get/suggestions$', views.getSuggestions, name='suggestions'),
    url(r'^post/schedule$', views._schedule, name='test'),
    url(r'^post/createlist$', views.createList, name='createlist'),
    url(r'^get/stats$', views.getStats, name='getstats'),
    url(r'^get/output$', views.output, name='getoutput'),
    url(r'^get/list$', views.lists, name='getoutput'),
    url(r'^get/temp$', views.temp, name='temp'),
]
