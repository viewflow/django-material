from .. import LiveTestCase


class Test(LiveTestCase):
    def test_checkboxinput(self):
        self.browser.get(f"{self.live_server_url}/widget/checkboxinput/")

        # check height
        fields = self.browser.find_elements_by_css_selector('.dmc-checkbox-field')
        self.assertEqual(
            {57.0},
            set(field.rect['height'] for field in fields)
        )

        # click on label
        checkbox = self.browser.find_element_by_css_selector('input[id="id_field1"]')
        label = self.browser.find_element_by_css_selector('label[for="id_field1"]')
        self.assertFalse(checkbox.is_selected())
        label.click()
        self.assertTrue(checkbox.is_selected())
