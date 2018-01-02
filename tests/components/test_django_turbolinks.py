from datetime import date

from tests.atlas.models import Continent, Country
from . import LiveTestCase


class Test(LiveTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.continent = Continent.objects.create(
            name="Africa",
            area="30370000",
            population=11000000000,
            population_density='4.2',
            longest_river='Irtysh',
            biggest_mountain='Neverest',
            hemisphere='BOTH'
        )
        self.country = Country.objects.create(
            code='RUS',
            name='Russian Federation',
            independence_day=date(1992, 6, 12),
            gay_friendly=False,
            continent=self.continent,
        )

    def test_turbolinks_init(self):
        self.assertTrue(self.login(username='admin', password='admin'))

        # initial non-turbolinks page load
        self.browser.get(f"{self.live_server_url}/atlas/country/")

        link = self.browser.find_element_by_css_selector('.dmc-list-table__cell-text a')
        link.click()

        result = self.browser.execute_script('''
            return Array.from(document.querySelectorAll("[data-mdc-auto-init]")).filter(
                function(elem) {return !(elem.dataset.mdcAutoInit in elem)}
            )
        ''')

        self.assertEqual(result, [])
        self.assertNoJsErrors()
