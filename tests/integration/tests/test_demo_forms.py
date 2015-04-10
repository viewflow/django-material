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
        form['password'] = ''
        form['keep_logged'] = 'aaa'

        response = form.submit()

        self.assertEquals('Enter a valid email address.', response.pyquery('#id_email_container .errors').text())
        self.assertEquals('This field is required.', response.pyquery('#id_password_container .errors').text())
