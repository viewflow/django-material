import os
import unittest

from selenium import webdriver
from needle.cases import NeedleTestCase
from needle.driver import (NeedleFirefox, NeedleChrome, NeedleIe, NeedleOpera,
                           NeedleSafari, NeedlePhantomJS)

from pyvirtualdisplay import Display
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


@unittest.skipUnless('VISUAL' in os.environ, 'Visual tests are not enabled')
class VisualTest(NeedleTestCase, StaticLiveServerTestCase):
    engine_class = 'needle.engines.perceptualdiff_engine.Engine'
    viewport_width = 1280
    viewport_height = 1024

    @classmethod
    def setUpClass(cls):
        cls.display = None
        if 'NODISPLAY' not in os.environ:
            cls.display = Display(visible=0, size=(cls.viewport_width, cls.viewport_height))
            cls.display.start()
        super(VisualTest, cls).setUpClass()

    @classmethod
    def set_viewport_size(cls, width, height):
        cls.driver.set_window_size(width, height)

    @classmethod
    def tearDownClass(cls):
        super(VisualTest, cls).tearDownClass()
        if cls.display is not None:
            cls.display.stop()

    @classmethod
    def get_web_driver(cls):
        """
        Returns the WebDriver instance to be used. Defaults to `NeedleFirefox()`.
        Override this method if you'd like to control the logic for choosing
        the proper WebDriver instance.
        """
        browser_name = os.environ.get('NEEDLE_BROWSER')
        browser_map = {
            'firefox': NeedleFirefox,
            'chrome': NeedleChrome,
            'ie': NeedleIe,
            'opera': NeedleOpera,
            'safari': NeedleSafari,
            'phantomjs': NeedlePhantomJS,
        }
        browser_class = browser_map.get(browser_name, NeedleFirefox)
        browser_kwargs = {}
        if browser_class == NeedleFirefox:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.startup.homepage", "about:blank")
            profile.set_preference("startup.homepage_welcome_url", "about:blank")
            profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")
            browser_kwargs = {'firefox_profile': profile}
        return browser_class(**browser_kwargs)

    def assertScreenshot(self, element_or_selector, file, threshold=0.02):
        super(VisualTest, self).assertScreenshot(element_or_selector, file, threshold=threshold)
