from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Bioenergie.views.home', name='home'),
    # url(r'^Bioenergie/', include('Bioenergie.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^customers/', include('Customer.urls')),
    url(r'^buildings/', include('Building.urls')),
    url(r'^counters/', include('Counter.urls')),
    url(r'^indexes/', include('Index.urls')),
    url(r'^measurements/', include('Measurement.urls')),
    url(r'^prices/', include('Price.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
