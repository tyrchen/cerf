from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cerf.views.common import IndexView, SigninView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 't.views.home', name='home'),
    # url(r'^t/', include('t.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url('^$', IndexView.as_view(), name="home"),
    url('^signin/$', SigninView.as_view(), name='signin'),
    url('^signout/$', 'django.contrib.auth.views.logout', name='signout'),
    url(r'^exams/', include('cerf.urls.exams')),
    url(r'^interviews/', include('cerf.urls.interviews')),
    url(r'^admin/', include(admin.site.urls)),
)
