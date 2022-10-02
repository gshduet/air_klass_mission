from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from core.models import TimeStampModel


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str = None, password: str = None) -> object:
        if not email:
            raise ValueError('EMAIL_IS_REQUIRED')

        user = self.model(
            email=email,
            username=username,
        )
        user.set_password(password)

        user.is_active = True
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False

        user.save(using=self._db)

        return user

    def create_superuser(self, username: str, email: str = None, password: str = None) -> object:
        if not email:
            raise ValueError('EMAIL_IS_REQUIRED')

        superuser = self.create_user(
            email=email,
            username=username,
            password=password,
        )

        superuser.is_active = True
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_superuser = True

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    SOCIAL_LOGIN_CHOICES = [
        ('DIRECT_SIGN_UP', 'direct'),
        ('KAKAO', 'kakao'),
        ('FACEBOOK', 'facebook'),
        ('APPLE', 'apple')
    ]

    user_type = models.CharField(
        max_length=20, choices=SOCIAL_LOGIN_CHOICES, default=SOCIAL_LOGIN_CHOICES[0])
    email = models.EmailField(
        max_length=127, unique=True, verbose_name='사용자 이메일')
    username = models.CharField(max_length=10, verbose_name='사용자 이름')
    is_master = models.BooleanField(default=False, verbose_name='강사유저 여부 확인')

    # AbstractBaseUser 등 Django Usermodel 작동을 위해 필요한 컬럼
    is_active = models.BooleanField(
        default=True, verbose_name='유저 계정 활성화 여부 확인')
    is_staff = models.BooleanField(
        default=False, verbose_name='관리자 페이지 접속 가능 여부 확인, 데이터 수정권한은 없음')
    is_admin = models.BooleanField(default=False, verbose_name='관리자 여부 확인')
    is_superuser = models.BooleanField(
        default=False, verbose_name='모든 권한을 가진 슈퍼유저 여부 확인')

    # UserManager.create_superuser 작동 시 email 입력을 위해 필요
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
