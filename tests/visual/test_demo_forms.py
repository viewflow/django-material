# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test.utils import override_settings
from . import VisualTest


@override_settings(ROOT_URLCONF='demo.tests.test_forms_login')
class TestLoginForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/login/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_login_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/login/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_login_invalid_data')


@override_settings(ROOT_URLCONF='demo.tests.test_forms_registration')
class TestRegistrationForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/registration/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_registration_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/registration/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_registration_invalid_data')


@override_settings(ROOT_URLCONF='demo.tests.test_forms_contact')
class TestContactForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/contact/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_contact_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/contact/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_contact_invalid_data')


@override_settings(ROOT_URLCONF='demo.tests.test_forms_order')
class TestOrderForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/order/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_order_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/order/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_order_invalid_data')


@override_settings(ROOT_URLCONF='demo.tests.test_forms_checkout')
class TestCheckoutForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/checkout/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_checkout_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/checkout/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_checkout_invalid_data')


@override_settings(ROOT_URLCONF='demo.tests.test_forms_comment')
class TestCommentForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/comment/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_comment_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/comment/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_comment_invalid_data')


@override_settings(ROOT_URLCONF='demo.tests.test_forms_bank')
class TestBankForm(VisualTest):
    def test_default_usecase(self):
        self.driver.get('%s/demo/bank/' % self.live_server_url)
        self.assertScreenshot('.card', 'form_bank_default_usecase')

    def test_invalid_data(self):
        self.driver.get('%s/demo/bank/' % self.live_server_url)

        self.driver.find_element_by_css_selector("button[type=submit]").click()
        self.assertScreenshot('.card', 'form_bank_invalid_data')
