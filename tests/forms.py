from django.template import Template

import tests.demo as forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    keep_logged = forms.BooleanField(required=False, label="Keep me logged in")

    template = Template("""
    {% with form_label_class="sr-only" form_control_class="floating-label" form_with_placeholder=True %}
    {% form %}
        {% part form.email prepend %}
            <span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
        {% endpart %}
        {% part form.password prepend %}
            <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
        {% endpart %}
        {% part form.keep_logged group_class %}form-group pull-right{% endpart %}
    {% endform %}
    {% endwith %}
    """)

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Login</button>
        <button class="btn btn-default pull-right">Register</button>
    """)

    title = "Login form"


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=(('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    template = Template("""
    {% with form_label_class="sr-only" form_control_class="floating-label" form_with_placeholder=True %}
    {% form %}
        {% part form.username prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-user"></i></span>
        {% endpart %}
        {% part form.email prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-inbox"></i></span>
        {% endpart %}
        {% part form.password prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-lock"></i></span>
        {% endpart %}
        {% part form.password_confirm prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-lock"></i></span>
        {% endpart %}
    {% endform %}
    {% endwith %}
    """)

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Submit</button>
    """)

    title = "Registration form"


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = forms.CharField(label="Enter characters below")
    send_copy = forms.BooleanField(required=False,
                                   label="Send a copy to my e-mail address")

    template = Template("""
    {% form %}
        {% part form.name append %}
            <span class="input-group-addon append"><i class="glyphicon glyphicon-user"></i></span>
        {% endpart %}
        {% part form.email append %}
            <span class="input-group-addon append"><i class="glyphicon glyphicon-envelope"></i></span>
        {% endpart %}
        {% part form.subject append %}
            <span class="input-group-addon append"><i class="glyphicon glyphicon-tag"></i></span>
        {% endpart %}
        #}
        {% part form.message rows %}4{% endpart %}
        {% part form.captcha append %}
            <span class="input-group-addon append">
                <img height="28px" src="http://image.captchas.net?client=demo&random=RandomZufall">
            </span>
        {% endpart %}
    {% endform %}
    """)

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Send message</button>
    """)

    title = "Contact form"


class OrderForm(forms.Form):
    name = forms.CharField()
    company = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    interest = forms.ChoiceField(choices=(('D', 'Design'), ('C', 'Development'), ('I', 'Illustration'),
                                          ('B', 'Branding'), ('V', 'Video')))
    bugget = forms.ChoiceField(choices=(('S', 'Less than $5000'), ('M', '$5000-$10000'),
                                        ('L', '$10000-$20000'), ('XL', 'More than $20000')))
    start_date = forms.DateField()
    finish_date = forms.DateField()

    attachment = forms.FileField()

    message = forms.CharField(widget=forms.Textarea)


class CheckoutForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    country = forms.ChoiceField(choices=())
    city = forms.CharField()
    post_code = forms.IntegerField()
    address = forms.CharField()
    additional_info = forms.CharField(widget=forms.Textarea)
    card_type = forms.ChoiceField(choices=(('V', 'Visa'), ('M', 'MasterCard'), ('P', 'Paypal')))
    card_holder = forms.CharField()
    card_number = forms.CharField()
    card_ccv2 = forms.IntegerField()
    card_exp_month = forms.ChoiceField(choices=((1, 'January'), (2, 'February'), (3, 'March'),
                                                (4, 'April'), (5, 'May'), (6, 'June'),
                                                (7, 'July'), (8, 'August'), (9, 'September'),
                                                (10, 'October'), (11, 'November'), (12, 'December')))
    card_exp_year = forms.IntegerField()
