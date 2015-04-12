from needle.cases import NeedleTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class VisualTest(NeedleTestCase, StaticLiveServerTestCase):
    def setUp(self):
        super(VisualTest, self).setUp()
        self.driver.set_window_size(1280, 1024)
