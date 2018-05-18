from django.contrib import admin
from blog.models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'modified_time', 'category', 'author']

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


