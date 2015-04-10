# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from needle.cases import NeedleTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestTextInputVisual(NeedleTestCase, StaticLiveServerTestCase):
    def test_default_usecase(self):
        self.driver.get('%s/demo/login/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_login_default_usecase', threshold=1)

    def test_invalid_data(self):
        self.driver.get('%s/demo/login/' % self.live_server_url)

        self.driver.find_element_by_css_selector("#id_email").send_keys('ё@admin.com')
        self.driver.find_element_by_css_selector("label[for=id_keep_logged]").click()

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_login_invalid_data', threshold=1)
