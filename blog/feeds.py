# '18-5-18' '下午4:40'
from django.contrib.syndication.views import Feed
from blog.models import Post


class AllPostRssFeed(Feed):
    title = 'Django 博客练手'

    link = '/'

    description = 'Django 博客'
    # 显示的内容条目

    def items(self):
        return Post.objects.all()
    # 聚合器中显示的内容条目标题

    def item_title(self, item):
        return '[{}]{}'.format(item.category, item.title)
    # 聚合器中显示的内容条目的描述

    def item_description(self, item):
        return item.body












