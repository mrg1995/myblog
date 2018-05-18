from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from comments.models import Comment
from comments.forms import CommentForm
# Create your views here.


def post_comment(request, post_pk):
    # 获得该评论的文章
    post = get_object_or_404(Post, pk=post_pk)
    print(post.tags)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            # 将评论和文章关联起来
            comment.post = post
            comment.save()
            # 当表单的数据合法时 重定向到post的详情页
            # 当redirect 函数接收一个模型的实例时, 会调用这个模型实例的get_absolute_url方法
            # 这个方法会返回一个url 然后重定向到这个url
            return redirect(post)
        else:
            #
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            print(post.tags)
            # 当表单数据不合法时,
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)







