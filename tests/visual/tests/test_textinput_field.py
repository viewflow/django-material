from needle.cases import NeedleTestCase
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from tests.integration.tests.test_textinput_field import TestTextInput


class TestTextInputVisual(NeedleTestCase, StaticLiveServerTestCase):
    urls = TestTextInput.urls
    driver = 'phantomjs'

    def test_test_default_usecase(self):
        self.driver.get('%s%s' % (self.live_server_url, TestTextInput.test_default_usecase.url))
        self.assertScreenshot('form', 'test_default_usecase')

    def test_missing_value_error_rendered(self):
        self.driver.get('%s%s' % (self.live_server_url, TestTextInput.test_missing_value_error_rendered.url))

        self.driver.find_element_by_css_selector("button").send_keys(Keys.RETURN)
        self.assertScreenshot('form', 'test_missing_value_error_rendered')

    def test_prefix_rendered(self):
        self.driver.get('%s%s' % (self.live_server_url, TestTextInput.test_prefix_rendered.url))
        self.assertScreenshot('form', 'test_prefix_rendered')

    def test_render_with_value(self):
        self.driver.get('%s%s' % (self.live_server_url, TestTextInput.test_render_with_value.url))
        self.driver.find_element_by_css_selector("input").send_keys('a'*21)
        self.driver.find_element_by_css_selector("button").send_keys(Keys.RETURN)
        self.assertScreenshot('form', 'test_render_with_value')
