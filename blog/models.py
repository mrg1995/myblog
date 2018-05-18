import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse


# 文章的分类


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 文章的标签


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 文章的具体信息


class Post(models.Model):
    title = models.CharField(max_length=70, help_text='文章标题')
    body = models.TextField(help_text='文章内容')
    created_time = models.DateTimeField(help_text='文章创建时间')
    modified_time = models.DateTimeField(help_text='文章最后一次修改时间')
    excerpt = models.CharField(max_length=200, blank=True, help_text='文章摘要,可以不写')
    category = models.ForeignKey('Category', help_text='文章的分类')
    tags = models.ManyToManyField('Tag', blank=True, help_text='文章的标签,可以为空')
    author = models.ForeignKey(User, help_text='使用auth模块')
    views = models.PositiveIntegerField(default=0, help_text='文章浏览量')

    def __str__(self):
        return self.title

    # @property
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 重写save方法 用来自动生成摘要
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 实例化一个markdown类  用来渲染body文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将body的markdown文本转成html文本, 然后去掉文本里的html标签,然后摘取前54个字符
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的save 方法 将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']



















