from .. import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def test_active_navigation(self):
        self.assertTrue(self.login(username='admin', password='admin'))

        # initial non-turbolinks page load
        self.browser.get(f"{self.live_server_url}/atlas/city/")
        page_menu = self.browser.find_element_by_css_selector('.dmc-list .dmc-list__menu-trigger')
        page_menu.click()

        # click
        menu = self.browser.find_element_by_css_selector('.dmc-list .mdc-simple-menu--open')
        self.assertTrue(menu.is_displayed())

        add_link = menu.find_element_by_css_selector('[data-dmc-menu-href="/atlas/city/add/"]')
        add_link.click()

        # add page loaded
        self.browser.find_element_by_css_selector('.dmc-form-page')

        self.assertNoJsErrors()
