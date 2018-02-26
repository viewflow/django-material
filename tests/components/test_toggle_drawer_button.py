from . import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.assertTrue(self.login(username='admin', password='admin'))
        self.browser.get(f"{self.live_server_url}/atlas/city/")

        self.drawer = self.browser.find_element_by_css_selector('.dmc-drawer')
        self.button = self.browser.find_element_by_css_selector(
            'a[data-controller="dmc-toggle-drawer-button"]'
        )

    def test_toggle_persistent_drawer(self):
        self.browser.set_window_size(1280, 947)
        drawer_classes = self.drawer.get_attribute('class').split(' ')
        self.assertIn('mdc-drawer--open', drawer_classes)

        self.button.click()
        drawer_classes = self.drawer.get_attribute('class').split(' ')
        self.assertNotIn('mdc-drawer--open', drawer_classes)

        self.button.click()
        drawer_classes = self.drawer.get_attribute('class').split(' ')
        self.assertIn('mdc-drawer--open', drawer_classes)

        self.assertNoJsErrors()

    def test_toggle_temporary_drawer(self):
        # temporary drawer
        self.browser.set_window_size(640, 480)
        drawer_classes = self.drawer.get_attribute('class').split(' ')
        self.assertNotIn('mdc-drawer--open', drawer_classes)

        self.button.click()
        drawer_classes = self.drawer.get_attribute('class').split(' ')
        self.assertIn('mdc-drawer--open', drawer_classes)

        self.assertNoJsErrors()
