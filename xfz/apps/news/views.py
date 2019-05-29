from django.shortcuts import render
from utils import restful
from .models import News,NewsCategory,Comment
from django.conf import settings
from .serializers import NewsSerializer,CommentSerializer
from django.http import Http404
from .forms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_require


def index(request):
    """
    首页数据渲染,渲染按时间排序
    :param request:
    :return:
    """
    count = settings.ONE_PAGE_NEWS_COUNT

    # 使用select_related查询页面中需要使用的外键,减少数据库的查询
    newses = News.objects.select_related('category','author').all()[0:count]

    # 新闻分类不会经常变化可以使用缓冲来保存
    categories = NewsCategory.objects.all()
    context = {
        'newses':newses,
        'categories':categories
    }
    return render(request,'news/index.html',context=context)


def news_list(request):
    """
    首页新闻展示,每次点击查看更多加载2(settings中指定的数量)篇文章
    :param request:新闻的页数
    :return:
    设置新闻的页数是通过地址栏中的查询字符串来传递 news/list/?p=1
    """
    page = int(request.GET.get('p',1))
    # 分类为0 表示当不进行任何筛选 默认按照时间进行排序
    category_id = int(request.GET.get('category_id',0))

    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        # 如果没有选择分类,默认是最新分类,查询展示所有分类
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        # 查询指定分类id
        newses = News.objects.select_related('category','author').filter(category__id=category_id)[start:end]

    # 使用rest_framework框架对查询的数据进行序列化,主要对返回使用外键查询的字段
    # 因为newses是查询出来的多个数据,是QuerySet对象，所以要添加many=True
    serializer = NewsSerializer(newses,many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request,news_id):

    try:
        news = News.objects.select_related('category','author').prefetch_related("comments__author").get(pk=news_id)
        # 评论可以通过Comment中的新闻id查询到
        # 也可以通过news.comment_set查询
        # comments = Comment.objects.select_related('author').filter(news_id=news.pk)
        context = {
            'news':news,
        }
        return render(request,'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404


@xfz_login_require
def public_comment(request):
    # 通过表单获取表单提交数据
    forms = PublicCommentForm(request.POST)
    # 验证表单数据
    if forms.is_valid():
        content = forms.cleaned_data.get('content')
        news_id = forms.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        # 保存评论数据
        comment = Comment.objects.create(
            content=content,
            news=news,
            author=request.user
        )
        # comment是一个对象,不需要添加many=True
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=forms.get_errors())



def search(request):
    return render(request,'search/search.html')
