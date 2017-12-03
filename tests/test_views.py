import unittest
from django.test import TestCase, Client
from unittest.mock import patch, Mock
import lxml.html as lh
from hamcrest import assert_that, none, not_none, is_, has_string
from instagram_auth.models import AccessToken


@patch('instagram_auth.views.InstagramAPI', autospec=True)
class InstagramAuthTest(TestCase):

    def configure_mock_instagram(self, mock_instagram, token=''):
        mock_instagram.return_value = Mock()
        mock_instagram_obj = mock_instagram.return_value
        mock_instagram_obj.exchange_code_for_access_token.return_value = {
            'access_token': token,
            'user': {
                'full_name': 'Concept Club',
                'id': '1574083',
                'profile_picture': '...',
                'username': 'concept_club'
            }
        }
        
        return mock_instagram, mock_instagram_obj

    def test_login_instagram_redirects(self, mock_instagram):
        mock_instagram, _ = self.configure_mock_instagram(mock_instagram)
        response = self.client.get('/accounts/oauth_callback/?code=secret')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_login_instagram_creates_token(self, mock_instagram):
        # empty database
        assert_that(AccessToken.objects.first(), is_(none()))
        token = 'fb2e77d.47a0479900504cb3ab4a1f626d174d2d'
        mock_instagram, mock_instagram_obj = self.configure_mock_instagram(mock_instagram,
                                                                           token=token)
        response = self.client.get('/accounts/oauth_callback/?code=secret')

        mock_instagram_obj.exchange_code_for_access_token.assert_called_once_with('secret')
        access_token = AccessToken.objects.first()
        assert_that(access_token, not_none, 'should store access_token')
        assert_that(access_token.access_token, is_(token))

