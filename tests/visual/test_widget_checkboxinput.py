from selenium.webdriver.common.keys import Keys

from django.test.utils import override_settings
from .. import test_widget_checkboxinput as test
from . import VisualTest


@override_settings(ROOT_URLCONF='tests.test_widget_checkboxinput')
class Test(VisualTest):
    def test_test_default_usecase(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_default_usecase.url))
        self.assertScreenshot('form', 'booleaninput_default_usecase')

    def test_invalid_value(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_invalid_value.url))
        self.driver.find_element_by_css_selector("button").send_keys(Keys.RETURN)
        self.assertScreenshot('form', 'booleaninput_missing_value_error')

    def test_part_group_class(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_group_class.url))
        self.assertScreenshot('form', 'booleaninput_part_group_class')

    def test_part_add_group_class(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_add_group_class.url))
        self.assertScreenshot('form', 'booleaninput_part_add_group_class')

    def test_part_prefix(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_prefix.url))
        self.assertScreenshot('form', 'booleaninput_part_prefix')

    def test_part_add_control_class(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_add_control_class.url))
        self.driver.find_element_by_css_selector("#id_test_field_container label").click()
        self.assertScreenshot('form', 'booleaninput_part_add_control_class')

    def test_part_label(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_label.url))
        self.assertScreenshot('form', 'booleaninput_part_label')

    def test_part_add_label_class(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_add_label_class.url))
        self.assertScreenshot('form', 'booleaninput_part_add_label_class')

    def test_part_help_text(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_help_text.url))        
        self.assertScreenshot('form', 'booleaninput_part_help_text')

    def test_part_errors(self):
        self.driver.get('%s%s' % (self.live_server_url, test.Test.test_part_errors.url))
        self.assertScreenshot('form', 'booleaninput_part_errors')
