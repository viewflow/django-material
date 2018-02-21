from .. import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def test_turbolinks_form(self):
        self.browser.get(f"{self.live_server_url}/accounts/login/")

        self.browser.execute_script('window.notReloaded = true;')

        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('admin')
        self.browser.find_element_by_css_selector('button[type=submit]').click()

        # wait for page load
        self.browser.find_element_by_css_selector('.dmc-drawer-header__avatar')

        self.assertTrue(
            self.browser.execute_script('return window.notReloaded')
        )

        self.assertNoJsErrors()
