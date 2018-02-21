from .. import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def test_header_menu(self):
        self.assertTrue(self.login(username='admin', password='admin'))
        self.browser.get(f"{self.live_server_url}/atlas/city/")

        primary_menu = self.browser.find_element_by_css_selector('.dmc-drawer__primary-content')
        secondary_menu = self.browser.find_element_by_css_selector('.dmc-drawer__secondary-content')
        button = self.browser.find_element_by_css_selector('.dmc-drawer-header__menu-button')

        self.assertTrue(primary_menu.is_displayed())
        self.assertFalse(secondary_menu.is_displayed())
        button.click()
        self.assertFalse(primary_menu.is_displayed())
        self.assertTrue(secondary_menu.is_displayed())

        self.assertNoJsErrors()
