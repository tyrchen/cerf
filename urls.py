from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cerf.views.common import IndexView, SigninView, SignoutView, StaticFileView
from django_markdown import flatpages

admin.autodiscover()
flatpages.register()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 't.views.home', name='home'),
                       # url(r'^t/', include('t.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url('^$', IndexView.as_view(), name="home"),
                       url('^signin/$', SigninView.as_view(), name='signin'),
                       url('^signout/$', SignoutView.as_view(), name='signout'),
                       url(r'^cases/', include('cerf.urls.cases')),
                       url(r'^exams/', include('cerf.urls.exams')),
                       url(r'^interviews/', include('cerf.urls.interviews')),
                       url(r'^api/', include('cerf.urls.api')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^markdown/', include('django_markdown.urls')),
                       )

urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^help/$', StaticFileView.as_view(filename='README.md'),
                            name='help'
                            ),
                        url(r'^release-notes/$',
                            StaticFileView.as_view(filename='release_notes.md'),
                            name='release_notes'),

                        url(r'^todo/$',
                            StaticFileView.as_view(filename='TODO.md'),
                            name='todo'),
                        )
