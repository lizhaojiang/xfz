from django.db import models



class CourseCategory(models.Model):
    """
    课程分类模型
    """
    name = models.CharField(max_length=100)


class Teacher(models.Model):
    """
    课程教师模型
    """
    username = models.CharField(max_length=100)
    avatar = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()



class Course(models.Model):
    """
    课程模型
    """
    title = models.CharField(max_length=100)
    category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher',on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

class CourseOrder(models.Model):
    course = models.ForeignKey('Course',on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('xfzauth.User',on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1表示支付宝支付 2表示微信支付
    istype = models.SmallIntegerField(default=0)
    # 1表示待支付  2表示支付成功
    status = models.SmallIntegerField(default=1)