from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from apps.course.forms import EditCourseCategoryForm
from apps.course.models import CourseCategory, Course, Teacher
from .forms import PubCourseForm
from utils import restful


class PubCourseView(View):
    """
    课程发布
    """
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }

        return render(request, 'cms/pub_course.html',context=context)

    def post(self,request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get("cover_url")
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(
                title=title,
                video_url=video_url,
                cover_url=cover_url,
                price=price,
                duration=duration,
                profile=profile,
                category=category,
                teacher=teacher
            )
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def course_category(request):
    """
    渲染新闻分类页面
    :param request: 请求所有分类数据
    :return: 返回所有分类
    """
    categories = CourseCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/course_category.html', context=context)

@require_POST
def add_course_category(request):
    """
    添加新闻分类后端验证,页面通过js弹窗实现
    :param request:
    :return:
    """
    # 获取数据
    name = request.POST.get('name')
    # 判断分类是否已经存在
    exists = CourseCategory.objects.filter(name=name).exists()
    if not exists:
        CourseCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在!')


@require_POST
def edit_course_category(request):
    """
    更新新闻分类后端逻辑,页面js弹窗实现
    :param request:
    :return:
    """
    form = EditCourseCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')

        try:
            # 查询传递的主键是否存在,如果存在就更新
            CourseCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存,无法更新')
    else:
        return restful.params_error(message=form.get_error())


@require_POST
def delete_course_category(request):
    """
    删除新闻分类,页面弹窗js实现
    :param request:
    :return:
    """
    pk = request.POST.get('pk')
    try:
        CourseCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message="该分类不存在!")
