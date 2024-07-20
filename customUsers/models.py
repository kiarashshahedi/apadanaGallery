from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    مدل کاربر سفارشی که از مدل پیش‌فرض کاربر جنگو ارث می‌برد.
    """
    user_guid = models.CharField(max_length=36, unique=True, null=True, blank=True)
    mobile_phone = models.CharField(max_length=15, unique=True)
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return self.username
