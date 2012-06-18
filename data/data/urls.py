from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'data.views.index'),
    url(r'^authenticate$', 'data.views.authenticate'),
    url(r'^admin/', include(admin.site.urls)),
)
