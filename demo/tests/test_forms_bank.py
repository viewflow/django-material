from django.conf.urls import url
from django.test.utils import override_settings
from django.views import generic
from django_webtest import WebTest
from .. import forms


@override_settings(ROOT_URLCONF=__name__)
class Test(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/bank/')

        form = page.form
        form['branch_name'] = 'Main branch'
        form['person_title'] = 'Mr'
        form['full_name'] = 'John Doe'
        form['date_of_birth'] = '1980-01-01'
        form['email'] = 'john@doe.com'
        form['parent_name'] = 'Will Doe'
        form['nationality'] = 42
        form['mobile_no'] = '5-555-4200-11'
        form['existing_bank_account'] = 'NO'
        form['partner_name'] = 'NO'
        form['flat_bulding'] = '11'
        form['road_no'] = 'NO'
        form['area_and_landmark'] = 'NO'
        form['city'] = 'Nowhere'
        form['telephone_residence'] = 'NO'
        form['office'] = 'NO'
        form['fax'] = 'NO'
        form['pin_code'] = 'NO'
        form['mailing_company_details'] = 'NO'
        form['mailing_road_no'] = 'NO'
        form['mailing_area_and_landmark'] = 'NO'
        form['mailing_city'] = 'NO'
        form['mailing_mobile'] = 'NO'
        form['mailing_telephone_residence'] = 'NO'
        form['mailing_office'] = 'NO'
        form['mailing_fax'] = 'NO'
        form['mailing_pin_code'] = 'NO'
        form['mailing_email'] = 'no@no.com'
        form['introducer_name'] = 'NO'
        form['introducer_account_no'] = 'NO'
        form['introducer_signature'] = 'NO'
        form['account_type'] = 'S'
        form['account_mode'] = 'CS'
        form['account_amount'] = 3000
        form['deposit_type'] = 'C'
        form['deposit_mode'] = 'CS'
        form['deposit_amount'] = 3000
        form['deposit_no'] = 'NO'
        form['deposit_individual_amount'] = 0
        form['occupation'] = 'NE'
        form['education'] = 'UG'
        form['montly_income'] = '000'
        form['job_title'] = 'NO'
        form['department'] = 'NO'
        form['nature_of_business'] = 'NO'
        form['martial_status'] = 'S'
        form['spouse_name'] = 'NO'
        form['other_account1'] = 'NO'
        form['other_account2'] = 'NO'
        form['reason'] = 'TEST'
        form['terms_accepted'] = 1

        response = form.submit()
        self.assertEqual(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/bank/')

        form = page.form

        form['date_of_birth'] = 'XXX'
        form['email'] = 'john'

        response = form.submit()
        self.assertEqual('This field is required.', response.pyquery('#id_branch_name_container .errors').text())
        self.assertEqual('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_other_account1_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_other_account2_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_road_no_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_telephone_residence_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_city_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_nature_of_business_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_office_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_account_type_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_email_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_introducer_name_container .errors').text())
        self.assertEqual('This field is required.',
                          response.pyquery('#id_deposit_individual_amount_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_deposit_no_container .errors').text())
        self.assertEqual('This field is required.',
                          response.pyquery('#id_mailing_company_details_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_city_container .errors').text())
        self.assertEqual('This field is required.',
                          response.pyquery('#id_mailing_telephone_residence_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_existing_bank_account_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_education_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_pin_code_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_flat_bulding_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_mobile_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_montly_income_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_road_no_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_deposit_type_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_spouse_name_container .errors').text())
        self.assertEqual('This field is required.',
                          response.pyquery('#id_mailing_area_and_landmark_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_introducer_signature_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_deposit_mode_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_nationality_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_martial_status_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_pin_code_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_account_amount_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_deposit_amount_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_occupation_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_full_name_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_partner_name_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_fax_container .errors').text())
        self.assertEqual('Enter a valid date.', response.pyquery('#id_date_of_birth_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_reason_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_branch_name_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_introducer_account_no_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_terms_accepted_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_job_title_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_department_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_area_and_landmark_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_fax_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_parent_name_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_account_mode_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mobile_no_container .errors').text())
        self.assertEqual('This field is required.', response.pyquery('#id_mailing_office_container .errors').text())


urlpatterns = [
    url(r'^demo/bank/$', generic.FormView.as_view(
        form_class=forms.BankForm, success_url='/demo/bank/', template_name="demo.html")),
]
