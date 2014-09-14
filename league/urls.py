from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
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
     url(r'^teams/$', 'teams.views.index'),
     url(r'^teams/(\d*)/', 'teams.views.show_week'),
     url(r'^teams/grid/', 'teams.views.grid'),




) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
