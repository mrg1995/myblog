import markdown
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
# Create your views here.

# 视图函数
# def index(request):
#     post_list = Post.objects.all()  # .order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# 视图函数转成类视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后 开启分页功能 值表示一页包含多少篇文章
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # 获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        # 用户当前请求的页码号
        page_number = page.number
        # 获得分页的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表 例如[1,2,3,4]
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number:page_number+2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number-3) if (page_number - 3) > 0 else 0:page_number-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number-3) if (page_number - 3) > 0 else 0:page_number-1]
            right = page_range[page_number:page_number+2]
            # 是否显示最后一页 和 最后一页之前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            # 是否显示第一页 和 第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


def detail(request, pk):
    # get_object_or_404 的作用就是 传入的pk 对应在 Post数据库表里是否有,有就返回对应的对象,没有就返回404错误 表示文章不存在
    post = get_object_or_404(Post, pk=pk)
    # 阅读量 +1
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 实例化一个 CommentForm 表单
    form = CommentForm()
    # 获取这篇文章下的所有评论
    comment_list = post.comment_set.all()
    # 将表单,文章,评论列表作为模板变量传给detail.html 模板
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 写get方法的目的是 文章阅读量的+1
        # get 方法返回一个HttpResponse 实例
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 文章阅读量加1
        # self.object 就是被访问的文章
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        # post.body = markdown.markdown(post.body,
        #                               extensions=[
        #                                   'markdown.extensions.extra',
        #                                   'markdown.extensions.codehilite',
        #                                   'markdown.extensions.toc',
        #                               ])
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        # 'markdown.extensions.toc',
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
# 按年月归档


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year)  # .order_by('-created_time')
    print(post_list)
    print(year, month)

    return render(request, 'blog/index.html', context={'post_list': post_list})


# class ArchivesView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#     def get_queryset(self):
#         create_time1 = get_object_or_404(Post, year=self.kwargs.get('create_time'))


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)  # .order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {
        'error_msg': error_msg,
        'post_list': post_list
    })




















