from django_webtest import WebTest


class TestLoginForm(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/login/')
        self.assertIn('id="id_email"', page.body.decode('utf-8'))
        self.assertIn('id="id_password"', page.body.decode('utf-8'))

        form = page.form
        form['email'] = 'admin@admin.com'
        form['password'] = 'admin'
        form['keep_logged'] = 1

        response = form.submit()

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/login/')

        form = page.form
        form['email'] = 'admin'
        form['keep_logged'] = 'aaa'

        response = form.submit()

        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_password_container .errors').text())


class TestRegistrationForm(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/registration/')

        form = page.form
        form['username'] = 'admin'
        form['email'] = 'admin@admin.com'
        form['password'] = 'admin'
        form['password_confirm'] = 'admin'
        form['first_name'] = 'Super'
        form['last_name'] = 'Admin'
        form['gender'] = 'M'
        form['receive_news'] = 1
        form['agree_toc'] = 1

        response = form.submit()

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/registration/')

        form = page.form
        form['email'] = 'admin'

        response = form.submit()

        self.assertEquals('This field is required.', response.pyquery('#id_username_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_password_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_password_confirm_container .errors').text())


class TestContactForm(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/contact/')

        form = page.form
        form['name'] = 'admin'
        form['email'] = 'admin@admin.com'
        form['subject'] = 'Test Message'
        form['message'] = 'Message body'
        form['send_copy'] = 1

        response = form.submit()

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/contact/')

        form = page.form
        form['email'] = 'admin'

        response = form.submit()

        self.assertEquals('This field is required.', response.pyquery('#id_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_subject_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_subject_container .errors').text())


class TestOrderForm(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/order/')

        form = page.form
        form['name'] = 'John Doe'
        form['company'] = 'Viewflow'
        form['email'] = 'john@viewflow.io'
        form['phone'] = '5-555-4200-11'
        form['interest'] = 'D'
        form['budget'] = 'S'
        form['start_date'] = '2015-06-01'
        form['finish_date'] = '2030-06-01'
        form['message'] = 'Test Message'

        response = form.submit(upload_files=[('attachment', __file__)])

        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/order/')

        form = page.form
        form['email'] = 'john'
        form['start_date'] = 'XXX'
        form['finish_date'] = 'XXX'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_company_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_phone_container .errors').text())
        self.assertEquals('Enter a valid date.', response.pyquery('#id_start_date_container .errors').text())
        self.assertEquals('Enter a valid date.', response.pyquery('#id_finish_date_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_message_container .errors').text())


class TestCheckoutForm(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/checkout/')

        form = page.form
        form['first_name'] = 'John'
        form['last_name'] = 'Doe'
        form['email'] = 'john@doe.com'
        form['phone'] = '5-555-4200-11'
        form['country'] = 4
        form['city'] = 'Proudvill'
        form['post_code'] = '00520'
        form['address'] = 'Nowhere St, 5'
        form['additional_info'] = 'No info'
        form['card_type'] = 'V'
        form['card_holder'] = 'JOHN DOE'
        form['card_number'] = 'XXXX XXXX XXXX XXXX'
        form['card_ccv2'] = '000'
        form['card_exp_month'] = '1'
        form['card_exp_year'] = '1970'

        response = form.submit()
        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/checkout/')

        form = page.form
        form['email'] = 'john'
        form['card_ccv2'] = 'john'
        form['card_exp_year'] = 'john'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_first_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_last_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_country_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_phone_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_city_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_post_code_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_address_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_additional_info_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_card_type_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_card_holder_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_card_number_container .errors').text())
        self.assertEquals('Enter a whole number.', response.pyquery('#id_card_ccv2_container .errors').text())
        self.assertEquals('Enter a whole number.', response.pyquery('#id_card_exp_year_container .errors').text())


class TestCommentForm(WebTest):
    def test_default_usecase(self):
        page = self.app.get('/demo/comment/')

        form = page.form
        form['name'] = 'John Doe'
        form['email'] = 'john@doe.com'
        form['website'] = 'http://me.johndoe'
        form['comment'] = 'Test comment'

        response = form.submit()
        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/comment/')

        form = page.form
        form['email'] = 'john'
        form['website'] = '_no_way_'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('Enter a valid URL.', response.pyquery('#id_website_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_comment_container .errors').text())


class TestBankForm(WebTest):
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
        self.assertEquals(302, response.status_code)

    def test_post_invalid_data(self):
        page = self.app.get('/demo/bank/')

        form = page.form
        form['date_of_birth'] = 'XXX'
        form['email'] = 'john'

        response = form.submit()
        self.assertEquals('This field is required.', response.pyquery('#id_branch_name_container .errors').text())
        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_other_account1_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_other_account2_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_road_no_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_telephone_residence_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_city_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_nature_of_business_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_office_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_account_type_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_introducer_name_container .errors').text())
        self.assertEquals('This field is required.',
                          response.pyquery('#id_deposit_individual_amount_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_deposit_no_container .errors').text())
        self.assertEquals('This field is required.',
                          response.pyquery('#id_mailing_company_details_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_city_container .errors').text())
        self.assertEquals('This field is required.',
                          response.pyquery('#id_mailing_telephone_residence_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_existing_bank_account_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_education_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_pin_code_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_flat_bulding_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_mobile_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_montly_income_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_road_no_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_deposit_type_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_spouse_name_container .errors').text())
        self.assertEquals('This field is required.',
                          response.pyquery('#id_mailing_area_and_landmark_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_introducer_signature_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_deposit_mode_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_nationality_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_martial_status_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_pin_code_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_account_amount_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_deposit_amount_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_occupation_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_full_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_partner_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_fax_container .errors').text())
        self.assertEquals('Enter a valid date.', response.pyquery('#id_date_of_birth_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_reason_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_branch_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_introducer_account_no_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_terms_accepted_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_job_title_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_department_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_area_and_landmark_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_fax_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_parent_name_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_account_mode_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mobile_no_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_mailing_office_container .errors').text())
