# '18-5-17' '下午11:03'
from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()

# 返回最新的5篇文章


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

# 按月归档 就是将文章按创建时间 降序排列(order='DESC'), 精确到月('month')


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

# 分类模板标签


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post'))  # .filter(num_post__gt=0)



