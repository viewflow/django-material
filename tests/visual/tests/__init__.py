from needle.cases import NeedleTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class VisualTest(NeedleTestCase, StaticLiveServerTestCase):
    engine_class = 'needle.engines.perceptualdiff_engine.Engine'
    viewport_width = 1280
    viewport_height = 1024

    def assertScreenshot(self, element_or_selector, file, threshold=0.5):
        super(VisualTest, self).assertScreenshot(element_or_selector, file, threshold=threshold)

