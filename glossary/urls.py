from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^social/', include('social_auth.urls')),
                       url(r'^login_error/', "main_app.views.login_error"),
                       url(r'^', include('main_app.urls')),
)