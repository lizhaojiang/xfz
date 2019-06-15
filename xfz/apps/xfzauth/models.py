from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField



class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        if not telephone:
            raise ValueError('请输入手机号!')
        if not username:
            raise ValueError('请输入用户名!')
        if not password:
            raise ValueError('请输入密码!')

        user = self.model(telephone=telephone,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password)

    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone,username,password)


class User(AbstractBaseUser,PermissionsMixin):
    # 不使用django自带的id自增为主键
    # 使用第三方的库创建唯一的主键 uuid
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=100)
    # password = models.CharField(max_length=200)
    email = models.EmailField(unique=True,null=True)
    # 是否是可用 默认是可用
    is_active = models.BooleanField(default=True)
    # 是否是是员工 默认不是 不能登陆后台
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    #更改唯一验证为手机号,django默认是username
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username






