from . import LiveTestCase


class Test(LiveTestCase):
    def test_textinput(self):
        self.browser.get(f"{self.live_server_url}/widget/textinput/")

        # check height
        fields = self.browser.find_elements_by_css_selector('.dmc-form-field')
        self.assertEqual(
            {76.0},
            set(field.rect['height'] for field in fields)
        )

        self.assertNoJsErrors()
