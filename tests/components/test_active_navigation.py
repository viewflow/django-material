from . import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def test_active_navigation(self):
        self.login(username='admin', password='admin')

        # initial non-turbolinks page load
        self.browser.get(f"{self.live_server_url}/atlas/city/")
        city_link = self.browser.find_element_by_xpath('//aside//a[@href="/atlas/city/"]')
        self.assertIn(
            'mdc-permanent-drawer--selected',
            city_link.get_attribute('class').split(' ')
        )

        # turbolinks based page load
        ocean_link = self.browser.find_element_by_xpath('//aside//a[@href="/atlas/ocean/"]')
        ocean_link.click()

        self.browser.find_element_by_xpath(
            '//aside//a[@href="/atlas/ocean/"][contains(@class, "mdc-permanent-drawer--selected")]'
        )
        self.assertNoJsErrors()
