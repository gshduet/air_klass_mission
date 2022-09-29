from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from core.models import TimeStampModel


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str = None, password: str = None) -> object:
        if not email:
            raise ValueError('EMAIL_IS_REQUIRED')

        user = self.model(
            user_type=User.SOCIAL_LOGIN_CHOICES[0],
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
            user_type=User.SOCIAL_LOGIN_CHOICES[0],
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


class User(AbstractBaseUser, TimeStampModel):
    """
    기존에 설정되어 있언 AbstractUser는 
    id / password / last_login / is_superuser / username / first_name / last_name / email / is_staff / is_active / date_joined
    등 경우에 따라 필요치 않은 컬럼들이 다수 포함되어 있어 
    id / password / last_login를 기본으로 하는 AbstractBaseUser로 변경하여 상속
    """
    SOCIAL_LOGIN_CHOICES = [
        ('DIRECT_SIGN_UP', 'direct'),
        ('KAKAO', 'kakao'),
        ('FACEBOOK', 'facebook'),
        ('APPLE', 'apple')
    ]  # 외부 API를 통해 가입한 사용자 구분을 위한 리스트

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
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'{self.email}-{self.username}'
