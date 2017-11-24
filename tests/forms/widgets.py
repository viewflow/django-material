from django import forms


class CheckboxInputForm(forms.Form):
    title = 'CheckboxInput'
    subtitle = 'Widget options demo'

    field1 = forms.BooleanField(help_text='default')
    field2 = forms.BooleanField(help_text='initial value', initial=True)
    field3 = forms.BooleanField(help_text='disabled', disabled=True)


class TextInputForm(forms.Form):
    title = "TextInput"
    subtitle = 'Widget options demo'

    field1 = forms.CharField(help_text='default')
    field2 = forms.CharField(help_text='initial value', initial="Initial value")
    field3 = forms.CharField(help_text='length between 5-10', min_length=5, max_length=10)
    field4 = forms.CharField(help_text='disabled', disabled=True, initial='Not editable')
    field5 = forms.CharField(help_text='prefix icon')


class SelectForm(forms.Form):
    title = "Select"
    subtitle = 'Widget options demo'

    CHOICES = (
        (None, 'Select a fruit'),
        (1, 'Apple'),
        (2, 'Orange'),
        (3, 'Watermeloun'))
    FLOAT_CHOICES = (
        (1.1, 'Perfect'),
        (1.0, 'Good'),
        (0.8, 'Bad'),
    )
    GROUPED_CHOICES = (
        (None, [(7, 'Mikhail')]),
        ('Team 1', [(1, 'Joe'), (2, 'Bob'), (3, 'Marie')]),
        ('Team 2', [(4, 'Anatoliy'), (5, 'Svetlana'), (6, 'Olga')]),
    )
    LONG_CHOICES = ((n, n) for n in range(100))

    field1 = forms.ChoiceField(help_text='default', choices=CHOICES)
    field2 = forms.ChoiceField(help_text='initial value', choices=CHOICES, initial=2)
    field3 = forms.ChoiceField(help_text='float choices', choices=FLOAT_CHOICES)
    field4 = forms.ChoiceField(help_text='groups', choices=GROUPED_CHOICES)
    field5 = forms.ChoiceField(help_text='long choices list', choices=LONG_CHOICES)
    field6 = forms.TypedChoiceField(help_text='cource to int', coerce=int, choices=CHOICES)
    field7 = forms.ChoiceField(help_text='prefix', choices=CHOICES)
