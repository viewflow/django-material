import os
import unittest

from needle.cases import NeedleTestCase
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
    def tearDownClass(cls):
        super(VisualTest, cls).tearDownClass()
        if cls.display is not None:
            cls.display.stop()

    def assertScreenshot(self, element_or_selector, file, threshold=0.05):
        super(VisualTest, self).assertScreenshot(element_or_selector, file, threshold=threshold)
