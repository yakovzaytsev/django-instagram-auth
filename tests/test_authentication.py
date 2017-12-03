from django.test import TestCase
from django.contrib.auth import get_user_model
from instagram_auth.authentication import InstagramAuthenticationBackend
from instagram_auth.models import AccessToken
User = get_user_model()


class AuthenticateTest(TestCase):

    def test_returns_new_user_if_token_exists(self):
        instagram_account = 'snoopdogg'
        access_token = AccessToken.objects.create(uid=instagram_account)
        user = InstagramAuthenticationBackend().authenticate(access_token.uid)
        new_user = User.objects.get(instagram_account=instagram_account)
        self.assertEqual(user, new_user)
