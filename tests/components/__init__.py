import os
import shutil
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver




@unittest.skipUnless(os.environ.get('SELENIUM'), 'Set SELENIUM=1 to run this test')
class LiveTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.assertTrue(shutil.which('geckodriver'), "`geckodriver` not found")

        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def assertNoJsErrors(self):
        errors = self.browser.execute_script('return window.errors')
        self.browser.execute_script('window.errors=[]')
        self.assertFalse(errors)
