from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib import auth # XXX

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)

class AccessToken(models.Model):
    uid = models.TextField(default='') # XXX instagram_account foreign key
    access_token = models.TextField(default='')


class UserManager(BaseUserManager):

    def crate_user(self, instagram_account):
        User.objects.create(instagram_account=instagram_account)

    def create_superuser(self, instagram_account, password):
        self.create_user(instagram_account)


class User(models.Model):
    instagram_account = models.TextField(unique=True, default='', primary_key=True) # TODO test unique

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'instagram_account'
    is_anonymous = False
    is_authenticated = True

    objects = UserManager()

    @property
    def is_staff(self):
        return self.instagram_account == getattr(settings, 'INSTAGRAM_STAFF_ACCOUNT', 'snoopdogg')

    @property
    def is_active(self):
        return True


