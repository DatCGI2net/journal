from django.conf.urls import url
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
url(r'^$', views.index, name='home'),
url(r'^blog/(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
url(r'^blog/(?P<post_id>[0-9]+)/comments/$', views.comments, name='comments'),
url(r'^blog/(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),


]
