from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
from apps.news.models import NewsCategory, News, Banner
from utils import restful
from .forms import EditNewsCategoryForm, WriteNewsForm, AddBannerForm, EditBannerForm, EditNewsForm
import os
import qiniu
from django.conf import settings
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse


@staff_member_required(login_url='index')
def index(request):
    """
    django自带的用户验证装饰器,如果不是超级员工(is_staff==0),就会跳转到指定的url中
    :param request: 验证用户是否登录
    :return: 未登录跳转到首页
    """
    return render(request, 'cms/index.html')


class NewsListView(View):
    def get(self, request):
        """
        后台新闻列表页面
        :page 页码,从地址栏获取
        :newses 需要分页的类
        :paginator 实例化分页的对象
        :page_obj 当前分页的对象
        """
        page = int(request.GET.get('p', 1))

        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0) or 0)
        newses = News.objects.select_related('category', 'author')

        # 判断查询日期是否传递 ,如果有按传递的值查询 如果只有开始日期那么结束日期默认就是当天日期 如果只有结束日期,开始日期就是指定日期
        if start or end:
            if start:
                start_date = datetime.strptime(start, "%Y/%m/%d")
            else:
                start_date = datetime(year=2019, month=1, day=1)

            if end:
                end_date = datetime.strptime(end, "%Y/%m/%d")
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        # 判断标题,如果存在就查询是否包含此title
        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, settings.ONE_PAGE_NEWS_LIST_COUNT)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'categories': NewsCategory.objects.all(),
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }
        context.update(context_data)

        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


class WriteNewsView(View):

    def get(self, request):
        """
        展示添加新闻页面
        :param request:
        :return:
        """
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        """
        接受页面数据,添加到数据库
        :param request:
        :return:
        """
        # 实例化表单模型
        form = WriteNewsForm(request.POST)
        # 验证表单信息
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)

            # 保存数据
            News.objects.create(
                title=title,
                desc=desc,
                thumbnail=thumbnail,
                content=content,
                category=category,
                author=request.user
            )
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


class EditNewsView(View):
    """
    修改新闻
    """

    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        # 获取数据
        form = EditNewsForm(request.POST)
        # 验证数据接收数据
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get('pk')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(
                title=title,
                desc=desc,
                thumbnail=thumbnail,
                content=content,
                category=category
            )
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
def delete_news(request):
    """
    删除新闻
    """
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()


@require_GET
def news_category(request):
    """
    渲染新闻分类页面
    :param request: 请求所有分类数据
    :return: 返回所有分类
    """
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)


@require_POST
def add_news_category(request):
    """
    添加新闻分类后端验证,页面通过js弹窗实现
    :param request:
    :return:
    """
    # 获取数据
    name = request.POST.get('name')
    # 判断分类是否已经存在
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在!')


@require_POST
def edit_news_category(request):
    """
    更新新闻分类后端逻辑,页面js弹窗实现
    :param request:
    :return:
    """
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')

        try:
            # 查询传递的主键是否存在,如果存在就更新
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存,无法更新')
    else:
        return restful.params_error(message=form.get_error())


@require_POST
def delete_news_category(request):
    """
    删除新闻分类,页面弹窗js实现
    :param request:
    :return:
    """
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message="该分类不存在!")


def banners(request):
    """
    轮播图管理
    :param request:
    :return:
    """
    return render(request, 'cms/banners.html')


def banner_list(request):
    """
    banner显示
    :param request:
    :return:
    """
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return restful.result(data=serializer.data)


def add_banner(request):
    """
    添加banner轮播图
    :param request:
    :return:
    """
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(
            priority=priority,
            image_url=image_url,
            link_to=link_to
        )
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.params_error(message=form.get_errors())
        pass


def delete_banner(request):
    """
    删除轮播图
    :param request:
    :return:
    """
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


def edit_banner(request):
    """
    修改轮播图
    :param request:
    :return:
    """
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.filter(pk=pk).update(
            priority=priority,
            image_url=image_url,
            link_to=link_to
        )
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


@require_POST
def upload_file(request):
    """
    上传缩略图
    :param request:
    :return:
    """
    # 获取上传的文件
    file = request.FILES.get('file')
    # 获取文件名称
    name = file.name
    # 遍历文件
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 构建完整的url链接 request.build_absolute_uri 生成当前项目的主url(host)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})


@require_GET
def qntoken(request):
    """
    配置七牛云,将上传的文件保存到七牛云
    :param request:
    :return:
    """
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    # 选择存储对象的地区名称
    bucket = settings.QINIU_BUCKET_NAME
    # 创建七牛存储对象
    q = qiniu.Auth(access_key, secret_key)
    # 获取token
    token = q.upload_token(bucket)
    # 返回前端token值
    return restful.result(data={'token': token})
