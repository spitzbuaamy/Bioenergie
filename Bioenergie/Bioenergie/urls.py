from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import Abrechnung

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Bioenergie.views.home', name='home'),
    # url(r'^Bioenergie/', include('Bioenergie.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^abrechnungen/', include('Abrechnung.urls')),
    url(r'^banks/', include('Bank.urls')),
    url(r'^basicprices/', include('BasicPrice.urls')),
    url(r'^bills/', include('Bill.urls')),
    url(r'^buildings/', include('Building.urls')),
    url(r'^cableprices/', include('CablePrice.urls')),
    url(r'^connectionflatrates/', include('ConnectionFlatRate.urls')),
    url(r'^counterbills/', include('CounterBill.urls')),
    url(r'^counterchanges/', include('CounterChange.urls')),
    url(r'^customers/', include('Customer.urls')),
    url(r'^indexes/', include('Index.urls')),
    url(r'^measurements/', include('Measurement.urls')),
    url(r'^measurementprices/', include('MeasurementPrice.urls')),
    url(r'^rates/', include('Rate.urls')),
    url(r'^workingprices/', include('WorkingPrice.urls')),
    url(r'^heatingplants/', include('HeatingPlant.urls')),
    url(r'^offers/', include('Offer.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$/', )
    url(r'^login/$', 'Abrechnung.views.user_login', name='login'),
    url(r'^logout/$', 'Abrechnung.views.user_logout', name='logout'),
)
