# '18-5-18' '上午10:26'
from django.conf.urls import url
from comments.views import *


# app_name = 'comments'

urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', post_comment, name='post_comment')
]















