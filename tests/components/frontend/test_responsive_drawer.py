from .. import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def test_responsive_drawer(self):
        self.assertTrue(self.login(username='admin', password='admin'))

        self.browser.set_window_size(1280, 947)
        self.browser.get(f"{self.live_server_url}/atlas/city/")

        drawer = self.browser.find_element_by_css_selector('.dmc-responsive-drawer')
        drawer_classes = drawer.get_attribute('class').split(' ')
        self.assertIn('mdc-persistent-drawer', drawer_classes)
        self.assertIn('mdc-persistent-drawer--open', drawer_classes)
        self.assertNotIn('mdc-temporary-drawer', drawer_classes)

        self.browser.set_window_size(640, 480)
        drawer_classes = drawer.get_attribute('class').split(' ')
        self.assertNotIn('mdc-persistent-drawer', drawer_classes)
        self.assertNotIn('mdc-persistent-drawer--open', drawer_classes)
        self.assertIn('mdc-temporary-drawer', drawer_classes)

        self.browser.set_window_size(1280, 947)
        drawer_classes = drawer.get_attribute('class').split(' ')
        self.assertIn('mdc-persistent-drawer', drawer_classes)
        self.assertIn('mdc-persistent-drawer--open', drawer_classes)
        self.assertNotIn('mdc-temporary-drawer', drawer_classes)

        self.assertNoJsErrors()
