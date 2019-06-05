import hashlib
import hmac
import os
import time
from django.shortcuts import render
from django.views import View
from django.conf import settings
from utils import restful
from .models import Course, Teacher,CourseOrder
from django.http import Http404
from .forms import WriteTeachForm, EditTeachForm
from apps.xfzauth.decorators import xfz_login_require

def course_index(request):
    """
    课程首页展示
    """
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    """
    课程详情页面
    """
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Http404

    context = {
        'course': course
    }

    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    """
    课程视频播放
    """
    # video：是视频文件的完整链接
    file = request.GET.get('video')

    # course_id = request.GET.get('course_id')
    # if not CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists():
    #     return restful.params_error(message='请先购买课程！')

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
def course_order(request,course_id):
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
        'course':course
    }
    return render(request,'course/course_order.html',context=context)


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
