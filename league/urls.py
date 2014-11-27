from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.shortcuts import redirect
import settings

# Uncomment the next two lines to enable the admin: 
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'league.views.home', name='home'),
    # url(r'^league/', include('league.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

     url(r'^signin/$', 'teams.views.signin'),
     url(r'^logout/$', 'teams.views.logout_user'),
     url(r'^mailing_list/$','teams.views.mailing_list'),

     url(r'^$', 'teams.views.show_all_leagues'),
     url(r'^public/', 'teams.views.show_global_leagues'),
     url(r'^espn/$', 'teams.views.espn_refresh'),
     url(r'^leagues/$', 'teams.views.get_all_leagues_json'),
     url(r'^global_leagues/$', 'teams.views.get_all_leagues_json', {"all": True}),
     url(r'^register/$', 'teams.views.register'),
     url(r'^register/signup/$', 'teams.views.signup'),

     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/$', 'teams.views.backbone'),
     url(r'^demo/$', 'teams.views.demo'),
     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/(\d*)/$', 'teams.views.get_team_report_card_json_view'),
     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/(\d*)/lineups/(\d*)', 'teams.views.show_week'),
     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/(\d*)/draft/(\d*)', 'teams.views.show_draftscore_week'),
     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/(\d*)/waiver/(\d*)', 'teams.views.show_waiver_week'),
     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/(\d*)/trade/(\d*)', 'teams.views.show_trade_week'),
     url(r'^leagues/espn/(\d*)/(\d\d\d\d)/(\d*)/draft/$', 'teams.views.get_'
                                                     'team_draft'),
     url(r'', include('social_auth.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
    (r'^django-rq/', include('django_rq.urls')),
)