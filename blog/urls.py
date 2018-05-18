# '18-5-17' '下午10:05'

from django.conf.urls import url
from blog.views import *


# app_name = 'blog'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryView.as_view(), name='category'),
    url(r'tag/(?P<pk>[0-9]+)/$', TagView.as_view(), name='tag'),

]
# archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/
# archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2}/


# url(r'^$', index, name='index'),
# url(r'^search/', search, name='search')


