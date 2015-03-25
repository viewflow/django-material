from django.template import Template
from material import Layout, Row, Column, Fieldset, Span2, Span4, Span5, Span10
import tests.demo as forms

COUNTRY_CHOICES = (
    (None, 'Country'), (244, 'Aaland Islands'), (1, 'Afghanistan'), (2, 'Albania'), (3, 'Algeria'),
    (4, 'American Samoa'), (5, 'Andorra'), (6, 'Angola'), (7, 'Anguilla'), (8, 'Antarctica'),
    (9, 'Antigua and Barbuda'), (10, 'Argentina'), (11, 'Armenia'), (12, 'Aruba'), (13, 'Australia'),
    (14, 'Austria'), (15, 'Azerbaijan'), (16, 'Bahamas'), (17, 'Bahrain'), (18, 'Bangladesh'),
    (19, 'Barbados'), (20, 'Belarus'), (21, 'Belgium'), (22, 'Belize'), (23, 'Benin'),
    (24, 'Bermuda'), (25, 'Bhutan'), (26, 'Bolivia'), (245, 'Bonaire, Sint Eustatius and Saba'),
    (27, 'Bosnia and Herzegovina'), (28, 'Botswana'), (29, 'Bouvet Island'), (30, 'Brazil'),
    (31, 'British Indian Ocean Territory'), (32, 'Brunei Darussalam'),
    (33, 'Bulgaria'), (34, 'Burkina Faso'), (35, 'Burundi'), (36, 'Cambodia'), (37, 'Cameroon'),
    (38, 'Canada'), (251, 'Canary Islands'), (39, 'Cape Verde'), (40, 'Cayman Islands'), (41, 'Central African Republic'),
    (42, 'Chad'), (43, 'Chile'), (44, 'China'), (45, 'Christmas Island'), (46, 'Cocos (Keeling) Islands'),
    (47, 'Colombia'), (48, 'Comoros'), (49, 'Congo'), (50, 'Cook Islands'), (51, 'Costa Rica'),
    (52, "Cote D'Ivoire"), (53, 'Croatia'), (54, 'Cuba'), (246, 'Curacao'), (55, 'Cyprus'),
    (56, 'Czech Republic'), (237, 'Democratic Republic of Congo'), (57, 'Denmark'), (58, 'Djibouti'), (59, 'Dominica'),
    (60, 'Dominican Republic'), (61, 'East Timor'), (62, 'Ecuador'), (63, 'Egypt'), (64, 'El Salvador'),
    (65, 'Equatorial Guinea'), (66, 'Eritrea'), (67, 'Estonia'), (68, 'Ethiopia'), (69, 'Falkland Islands (Malvinas)'),
    (70, 'Faroe Islands'), (71, 'Fiji'), (72, 'Finland'), (74, 'France, skypolitan'), (75, 'French Guiana'),
    (76, 'French Polynesia'), (77, 'French Southern Territories'), (126, 'FYROM'), (78, 'Gabon'), (79, 'Gambia'),
    (80, 'Georgia'), (81, 'Germany'), (82, 'Ghana'), (83, 'Gibraltar'), (84, 'Greece'),
    (85, 'Greenland'), (86, 'Grenada'), (87, 'Guadeloupe'), (88, 'Guam'), (89, 'Guatemala'),
    (241, 'Guernsey'), (90, 'Guinea'), (91, 'Guinea-Bissau'), (92, 'Guyana'), (93, 'Haiti'),
    (94, 'Heard and Mc Donald Islands'), (95, 'Honduras'), (96, 'Hong Kong'), (97, 'Hungary'), (98, 'Iceland'),
    (99, 'India'), (100, 'Indonesia'), (101, 'Iran (Islamic Republic of)'), (102, 'Iraq'), (103, 'Ireland'),
    (104, 'Israel'), (105, 'Italy'), (106, 'Jamaica'), (107, 'Japan'), (240, 'Jersey'),
    (108, 'Jordan'), (109, 'Kazakhstan'), (110, 'Kenya'), (111, 'Kiribati'), (113, 'Korea, Republic of'),
    (114, 'Kuwait'), (115, 'Kyrgyzstan'), (116, "Lao People's Democratic Republic"), (117, 'Latvia'), (118, 'Lebanon'),
    (119, 'Lesotho'), (120, 'Liberia'), (121, 'Libyan Arab Jamahiriya'), (122, 'Liechtenstein'), (123, 'Lithuania'),
    (124, 'Luxembourg'), (125, 'Macau'), (127, 'Madagascar'), (128, 'Malawi'), (129, 'Malaysia'),
    (130, 'Maldives'), (131, 'Mali'), (132, 'Malta'), (133, 'Marshall Islands'), (134, 'Martinique'),
    (135, 'Mauritania'), (136, 'Mauritius'), (137, 'Mayotte'), (138, 'Mexico'), (139, 'Micronesia, Federated States of'),
    (140, 'Moldova, Republic of'), (141, 'Monaco'), (142, 'Mongolia'), (242, 'Montenegro'), (143, 'Montserrat'),
    (144, 'Morocco'), (145, 'Mozambique'), (146, 'Myanmar'), (147, 'Namibia'), (148, 'Nauru'),
    (149, 'Nepal'), (150, 'Netherlands'), (151, 'Netherlands Antilles'), (152, 'New Caledonia'), (153, 'New Zealand'),
    (154, 'Nicaragua'), (155, 'Niger'), (156, 'Nigeria'), (157, 'Niue'), (158, 'Norfolk Island'),
    (112, 'North Korea'), (159, 'Northern Mariana Islands'), (160, 'Norway'), (161, 'Oman'), (162, 'Pakistan'),
    (163, 'Palau'), (247, 'Palestinian Territory, Occupied'), (164, 'Panama'), (165, 'Papua New Guinea'), (166, 'Paraguay'),
    (167, 'Peru'), (168, 'Philippines'), (169, 'Pitcairn'), (170, 'Poland'), (171, 'Portugal'),
    (172, 'Puerto Rico'), (173, 'Qatar'), (174, 'Reunion'), (175, 'Romania'), (176, 'Russian Federation'),
    (177, 'Rwanda'), (178, 'Saint Kitts and Nevis'), (179, 'Saint Lucia'), (180, 'Saint Vincent and the Grenadines'),
    (181, 'Samoa'), (182, 'San Marino'), (183, 'Sao Tome and Principe'), (184, 'Saudi Arabia'), (185, 'Senegal'),
    (243, 'Serbia'), (186, 'Seychelles'), (187, 'Sierra Leone'), (188, 'Singapore'), (189, 'Slovak Republic'),
    (190, 'Slovenia'), (191, 'Solomon Islands'), (192, 'Somalia'), (193, 'South Africa'),
    (194, 'South Georgia &amp; South Sandwich Islands'), (248, 'South Sudan'), (195, 'Spain'), (196, 'Sri Lanka'),
    (249, 'St. Barthelemy'), (197, 'St. Helena'), (250, 'St. Martin (French part)'), (198, 'St. Pierre and Miquelon'),
    (199, 'Sudan'), (200, 'Suriname'), (201, 'Svalbard and Jan Mayen Islands'), (202, 'Swaziland'),
    (203, 'Sweden'), (204, 'Switzerland'), (205, 'Syrian Arab Republic'), (206, 'Taiwan'), (207, 'Tajikistan'),
    (208, 'Tanzania, United Republic of'), (209, 'Thailand'), (210, 'Togo'), (211, 'Tokelau'), (212, 'Tonga'),
    (213, 'Trinidad and Tobago'), (214, 'Tunisia'), (215, 'Turkey'), (216, 'Turkmenistan'),
    (217, 'Turks and Caicos Islands'), (218, 'Tuvalu'), (219, 'Uganda'), (220, 'Ukraine'), (221, 'United Arab Emirates'),
    (222, 'United Kingdom'), (223, 'United States'), (224, 'United States Minor Outlying Islands'), (225, 'Uruguay'),
    (226, 'Uzbekistan'), (227, 'Vanuatu'), (228, 'Vatican City State (Holy See)'), (229, 'Venezuela'), (230, 'Viet Nam'),
    (231, 'Virgin Islands (British)'), (232, 'Virgin Islands (U.S.)'), (233, 'Wallis and Futuna Islands'),
    (234, 'Western Sahara'), (235, 'Yemen'), (238, 'Zambia'), (239, 'Zimbabwe'),
)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    keep_logged = forms.BooleanField(required=False, label="Keep me logged in")

    template = Template("""
    {% form %}
        {% part form.email prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% part form.password prefix %}<i class="mdi-action-lock prefix"></i>{% endpart %}
        {% part form.keep_logged add_group_class %}right-align{% endpart %}
    {% endform %}
    """)

    buttons = Template("""
        <button class="waves-effect waves-teal btn-flat">Register</button>
        <button class="waves-effect waves-light btn" type="submit">Login</button>
    """)

    title = "Login form"


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Pesonal details',
                             Row('first_name', 'last_name'),
                             'gender', 'receive_news', 'agree_toc'))

    template = Template("""
    {% form %}
        {% part form.username prefix %}<i class="mdi-action-account-box prefix"></i>{% endpart %}
        {% part form.email prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% part form.password prefix %}<i class="mdi-action-lock-open prefix"></i>{% endpart %}
    {% endform %}
    """)

    buttons = Template("""
        <button class="waves-effect waves-light btn" type="submit">Submit</button>
    """)

    title = "Registration form"


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    send_copy = forms.BooleanField(required=False,
                                   label="Send a copy to my e-mail address")

    template = Template("""
    {% form %}
        {% part form.name prefix %}<i class="mdi-action-account-box prefix"></i>{% endpart %}
        {% part form.email prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% part form.subject prefix %}<i class="mdi-action-announcement prefix"></i>{% endpart %}
        {% part form.message prefix %}<i class="mdi-communication-message prefix"></i>{% endpart %}
        {% part form.send_copy add_group_class %}right-align{% endpart %}
    {% endform %}
    """)

    layout = Layout(Row('name', 'email'), 'subject', 'message', 'send_copy')

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Send message</button>
    """)

    title = "Contact form"


class OrderForm(forms.Form):
    name = forms.CharField()
    company = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    interest = forms.ChoiceField(choices=((None, 'Interested in'), ('D', 'Design'), ('C', 'Development'),
                                          ('I', 'Illustration'), ('B', 'Branding'), ('V', 'Video')))
    budget = forms.ChoiceField(choices=((None, 'Budget'), ('S', 'Less than $5000'), ('M', '$5000-$10000'),
                                        ('L', '$10000-$20000'), ('XL', 'More than $20000')))
    start_date = forms.DateField(label="Expected start date")
    finish_date = forms.DateField(label="Expected finish date")

    attachment = forms.FileField(label="Include some file...")

    message = forms.CharField(widget=forms.Textarea)

    layout = Layout('name', 'company', 'email', 'phone',
                    Row('interest', 'budget'),
                    Row('start_date', 'finish_date'),
                    'attachment', 'message')

    template = Template("""
    {% form %}
        {% part form.name prefix %}<i class="mdi-action-account-box prefix"></i>{% endpart %}
        {% part form.company prefix %}<i class="mdi-communication-business prefix"></i>{% endpart %}
        {% part form.email prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% part form.phone prefix %}<i class="mdi-communication-call prefix"></i>{% endpart %}

    {% endform %}
    """)

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Submit request</button>
    """)

    title = "Order services"


class CheckoutForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    city = forms.CharField()
    post_code = forms.IntegerField()
    address = forms.CharField()
    additional_info = forms.CharField(widget=forms.Textarea)
    card_type = forms.ChoiceField(choices=(('V', 'Visa'), ('M', 'MasterCard'), ('P', 'Paypal')), widget=forms.RadioSelect)
    card_holder = forms.CharField(label="Name on card")
    card_number = forms.CharField(label="Card number")
    card_ccv2 = forms.IntegerField(label="CVV2")
    card_exp_month = forms.ChoiceField(choices=((1, 'January'), (2, 'February'), (3, 'March'),
                                                (4, 'April'), (5, 'May'), (6, 'June'),
                                                (7, 'July'), (8, 'August'), (9, 'September'),
                                                (10, 'October'), (11, 'November'), (12, 'December')))
    card_exp_year = forms.IntegerField(label="Year")

    layout = Layout(
        Row('first_name', 'last_name'),
        Row('email', 'phone'),
        Row(Span5('country'), Span5('city'), Span2('post_code')),
        'address',
        'additional_info',
        Fieldset('Card Details',
                 Row(Column('card_type', span_columns=4),
                     Column('card_holder',
                            Row(Span10('card_number'), Span2('card_ccv2')),
                            Row('card_exp_month', 'card_exp_year'),
                            span_columns=8))))

    template = Template("""
    {% form %}
        {% part form.first_name prefix %}<i class="mdi-action-account-box prefix"></i>{% endpart %}
        {% part form.last_name prefix %}<i class="mdi-action-account-box prefix"></i>{% endpart %}
        {% part form.email prefix %}<i class="mdi-communication-email prefix"></i>{% endpart %}
        {% part form.phone prefix %}<i class="mdi-communication-call prefix"></i>{% endpart %}
        {% part form.card_type add_group_class2 %}inline{% endpart %}
    {% endform %}
    """)

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Submit request</button>
    """)

    title = "Checkout form"


class CommentForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    website = forms.URLField()
    comment = forms.CharField(widget=forms.Textarea)
    captcha = forms.CharField(label="Enter characters below")

    layout = Layout(Row('name', 'email'),
                    'website', 'comment', 'captcha')

    template = Template("""
    {% with form_label_class="sr-only" form_control_class="floating-label" form_with_placeholder=True %}
    {% form %}
        {% part form.comment rows %}4{% endpart %}
        {% part form.name prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-user"></i></span>
        {% endpart %}
        {% part form.email prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-envelope"></i></span>
        {% endpart %}
        {% part form.website prepend %}
            <span class="input-group-addon prepend"><i class="glyphicon glyphicon-briefcase"></i></span>
        {% endpart %}
        {% part form.captcha append %}
            <span class="input-group-addon append">
                <img height="28px" src="http://image.captchas.net?client=demo&random=RandomZufall">
            </span>
        {% endpart %}
    {% endform %}
    {% endwith %}
    """)

    buttons = Template("""
        <button class="btn btn-primary pull-right" type="submit">Add comment</button>
    """)

    title = "Comment form"
