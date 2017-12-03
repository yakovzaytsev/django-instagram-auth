from django.test import TestCase
from django.contrib import auth
from instagram_auth.models import AccessToken
User = auth.get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_instagram_account_only(self):
        user = User(instagram_account='snoopdogg')
        user.full_clean() # should not raise

    def test_instagram_account_is_primary_key(self):
        user = User(instagram_account='snoopdogg')
        self.assertEqual(user.pk, 'snoopdogg')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(instagram_account='snoopdogg')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user) # should not raise


class AccessTokenTest(TestCase):

    def test_links_user_with_generated_token(self):
        # TODO
        pass

