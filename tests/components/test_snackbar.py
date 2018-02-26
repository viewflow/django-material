from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import LiveTestCase


class Test(LiveTestCase):
    def test_snackbar(self):
        self.browser.get(f"{self.live_server_url}/components/snackbar/")

        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'mdc-snackbar__action-button'))
        )

        snackbar_text = self.browser.find_element_by_css_selector('.mdc-snackbar__text')
        self.assertEqual(snackbar_text.text, 'Test message')
        button.click()

        # snackbar action redirects to /page/404/
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'dmc-lockscreen__action'))
        )
        self.assertEqual(f"{self.live_server_url}/page/404/", self.browser.current_url)

        self.assertNoJsErrors()
