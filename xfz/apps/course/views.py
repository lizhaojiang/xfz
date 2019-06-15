import hashlib
import hmac
import os
import time
from hashlib import md5
from django.shortcuts import reverse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from utils import restful
from .models import Course, Teacher, CourseOrder
from django.http import Http404
from .forms import WriteTeachForm, EditTeachForm
from apps.xfzauth.decorators import xfz_login_require
from django.views.decorators.csrf import csrf_exempt


def course_index(request):
    """
    课程首页展示
    """
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'course/course_index.html', context=context)


@xfz_login_require
def course_detail(request, course_id):
    """
    课程详情页面
    """
    try:
        course = Course.objects.get(pk=course_id)
        buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
    except Course.DoesNotExist:
        return Http404

    context = {
        'course': course,
        'buyed': buyed
    }

    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    """
    课程视频播放
    """
    # video：是视频文件的完整链接
    file = request.GET.get('video')

    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists():
        return restful.params_error(message='请先购买课程！')

    expiration_time = int(time.time()) + 2 * 60 * 60
    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY
    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')
    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})


@xfz_login_require
def course_order(request, course_id):
    """
    课程支付
    """
    course = Course.objects.get(pk=course_id)

    order = CourseOrder.objects.create(
        course=course,
        buyer=request.user,
        status=1,
        amount=course.price,

    )

    context = {
        'goods': {
            'thumbnail': course.cover_url,
            'title': course.title,
            'price': course.price
        },
        'order': order,
        'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
        'return_url': request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))
    }
    return render(request, 'course/course_order.html', context=context)


@xfz_login_require
def course_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = '210fd55b8c1fa057a0809d5d19cf2e2e'
    uid = 'f8d2f709829d5994574e61c0'
    orderuid = str(request.user.pk)

    print('goodsname:', goodsname)
    print('istype:', istype)
    print('notify_url:', notify_url)
    print('orderid:', orderid)
    print('price:', price)
    print('return_url:', return_url)

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    print('key:', key)

    return restful.result(data={"key": key})


# 装饰器表示是去除csrf保护
@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    # print('='*10)
    # print(orderid)
    # print('='*10)
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()


class AddTeachView(View):
    """
    添加教师
    """

    def get(self, request):
        return render(request, 'course/write_teach.html')

    def post(self, request):
        form = WriteTeachForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            avatar = form.cleaned_data.get('avatar')
            jobtitle = form.cleaned_data.get('jobtitle')
            profile = form.cleaned_data.get('profile')

            Teacher.objects.create(
                username=username,
                avatar=avatar,
                jobtitle=jobtitle,
                profile=profile
            )

            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# 还没完成
class EditTeachView(View):
    """
    修改教师
    """

    def get(self, request):
        teacher_id = request.GET.get('teacher_id')
        teachers = Teacher.objects.get(pk=teacher_id)
        context = {
            'teachers': teachers,
        }
        return render(request, 'course/write_teach.html', context=context)

    def post(self, request):
        # 获取数据
        form = EditTeachForm(request.POST)
        # 验证数据接收数据
        if form.is_valid():
            username = form.cleaned_data.get('username')
            avatar = form.cleaned_data.get('avator')
            jobtitle = form.cleaned_data.get('jobtitle')
            profile = form.cleaned_data.get('profile')
            pk = form.cleaned_data.get('pk')

            Teacher.objects.filter(pk=pk).update(
                username=username,
                avatar=avatar,
                jobtitle=jobtitle,
                profile=profile
            )
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


class TeachListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()

        context = {
            'teachers': teachers
        }
        return render(request, 'course/teach_list.html', context=context)
