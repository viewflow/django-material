from django_webtest import WebTest


class Test(WebTest):
    def test_login_form(self):
        page = self.app.get('/demo/login/')

        form = page.form
        form['email'] = 'admin@admin.com'
        form['password'] = 'password'
        form['keep_logged'] = 1

        response = form.submit()

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['form'].is_valid())

    def test_contact_form(self):
        page = self.app.get('/demo/contact/')

        form = page.form
        form['name'] = 'John Doe'
        form['email'] = 'john@doe.com'
        form['subject'] = "What's up!"
        form['message'] = "Hey!"
        form['send_copy'] = 1

        response = form.submit()

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['form'].is_valid())

    def test_registration_form(self):
        page = self.app.get('/demo/registration/')

        form = page.form
        form['username'] = 'johndoe'
        form['email'] = 'john@doe.com'
        form['password'] = '123456'
        form['password_confirm'] = '123456'
        form['first_name'] = 'John'
        form['last_name'] = 'Doe'
        form['gender'] = 'O'
        form['receive_news'] = 0
        form['agree_toc'] = 1

        response = form.submit()

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['form'].is_valid())
