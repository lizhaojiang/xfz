from django.db import models
from shortuuidfield import ShortUUIDField


# Create your models here.
class Payinfo(models.Model):
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    price = models.FloatField()
    path = models.FilePathField()


class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey('Payinfo', on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 0表示支付宝支付 1表示微信支付
    istype = models.SmallIntegerField(default=0)
    # 1表示待支付  2表示支付成功
    status = models.SmallIntegerField(default=1)
