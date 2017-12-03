import sys
from instagram_auth.models import User, AccessToken

class InstagramAuthenticationBackend(object):

    def authenticate(self, uid): # instagram_account
        token = AccessToken.objects.get(uid=uid)
        try:
            user = User.objects.get(instagram_account=token.uid)
            return user
        except User.DoesNotExist:
            return User.objects.create(instagram_account=token.uid)

    def get_user(self, instagram_account):
        return User.objects.get(instagram_account=instagram_account)
