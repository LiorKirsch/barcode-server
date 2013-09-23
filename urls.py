from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'barcodeServer.views.home', name='home'),
    # url(r'^barcodeServer/', include('barcodeServer.foo.urls')),

    url(r'^barcodeServer/uploadImage$', 'barcodeServer.views.uploadImage'),
    url(r'^barcodeServer/uploadBarcode$', 'barcodeServer.views.uploadBarcode'),
    url(r'^barcodeServer/addProductDetails/(?P<productBarCode>\w+)', 'barcodeServer.views.addProductDetails'),
    url(r'^barcodeServer/addToPerson/(?P<personID>\w+)', 'barcodeServer.views.addToPerson'),
    url(r'^barcodeServer/getRecords$', 'barcodeServer.views.getRecords'),
    url(r'^$', 'barcodeServer.views.base', name='base'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
