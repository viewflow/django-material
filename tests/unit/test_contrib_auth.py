from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, path, reverse

from material.contrib.auth import AuthViewset


@override_settings(ROOT_URLCONF=__name__)
class Test(TestCase):
    def test_all_url_resolved(self):
        self.assertEqual(
            '/accounts/login/', reverse('login'))
        self.assertEqual(
            '/accounts/logout/', reverse('logout'))
        self.assertEqual(
            '/accounts/password_change/', reverse('password_change'))
        self.assertEqual(
            '/accounts/password_change/done/', reverse('password_change_done'))
        self.assertEqual(
            '/accounts/password_reset/', reverse('password_reset'))
        self.assertEqual(
            '/accounts/password_reset/done/', reverse('password_reset_done'))
        self.assertEqual(
            '/accounts/reset/DEADBEAF/0-o/',
            reverse('password_reset_confirm', args=['DEADBEAF', '0-o']))
        self.assertEqual(
            '/accounts/reset/done/', reverse('password_reset_complete'))

    def test_disable_password_reset(self):
        self.assertEqual(
            '/nopass/login/', reverse('nopass:login'))
        self.assertEqual(
            '/nopass/logout/', reverse('nopass:logout'))
        with self.assertRaises(NoReverseMatch):
            reverse('nopass:password_change')
        with self.assertRaises(NoReverseMatch):
            reverse('nopass:password_change_done')
        with self.assertRaises(NoReverseMatch):
            reverse('nopass:password_reset')
        with self.assertRaises(NoReverseMatch):
            reverse('nopass:password_reset_done')
        with self.assertRaises(NoReverseMatch):
            reverse('nopass:password_reset_confirm', args=['DEADBEAF', '0-o'])
        with self.assertRaises(NoReverseMatch):
            reverse('nopass:password_reset_complete')


urlpatterns = [
    path('accounts/', AuthViewset().urls),
    path('nopass/', AuthViewset(
        allow_password_change=False,
        app_name='nopass'
    ).urls)
]
