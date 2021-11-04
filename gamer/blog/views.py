from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import BlogType, Blog
from comment.models import Comment

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    # 对博客进行分页
    paginator = Paginator(blogs_all_list, 5)
    # 获取url中的页面参数
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    page_range = [x for x in range(int(page_num) - 2, int(page_num) + 3) if 0 < x <= paginator.num_pages]
    # 加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 获取分类数量
    blog_types = BlogType.objects.all()

    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = blog_types
    # context['blogs_dates'] = Blog.objects.date('created_time', order='DESC')
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    blog_content_type = ContentType.objects.get_for_model(blog)
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        blog.read_num += 1
        blog.save()

    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog_pk)

    context = {}
    context['blog'] = blog
    context['comments'] = comments
    response = render(request, 'blog/blog_detail.html', context)  # 响应
    response.set_cookie('blog_%s_read' % blog_pk, 'true', max_age=3600)
    return response


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blog_type'] = blog_type
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blogs_types'] = BlogType.objects.all()
    return render(request, 'blog/blogs_with_type.html', context)

# Create your views here.
