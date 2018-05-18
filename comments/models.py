from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=100, help_text='用户名称')
    email = models.EmailField(max_length=255, help_text='用户邮箱')
    url = models.URLField(blank=True, help_text='个人网站')
    text = models.TextField(help_text='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, help_text='评论时间')
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]











