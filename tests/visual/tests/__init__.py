from needle.cases import NeedleTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class VisualTest(NeedleTestCase, StaticLiveServerTestCase):
    engine_class = 'needle.engines.perceptualdiff_engine.Engine'
    viewport_width = 1280
    viewport_height = 1024
