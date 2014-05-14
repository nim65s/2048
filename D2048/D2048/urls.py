from django.conf.urls import patterns, include, url

from .views import GridCreateView, GridDetailView, GridMoveView, GridSaveView

urlpatterns = patterns('',
        url(r'', include('django.contrib.staticfiles.urls')),

        url(r'^$', GridCreateView.as_view(), name='create'),
        url(r'^(?P<pk>\d+)$', GridDetailView.as_view(), name='detail'),
        url(r'^save/(?P<pk>\d+)$', GridSaveView.as_view(), name='save'),
        url(r'^move/(?P<pk>\d+)/(?P<dir>\d)$', GridMoveView.as_view(), name='move'),
)
