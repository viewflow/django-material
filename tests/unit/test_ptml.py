from django.test import TestCase
from material import ptml


class Test(TestCase):
    def test_element_without_body(self):
        element = ptml.Div()
        self.assertEqual(str(element), '<div></div>')

    def test_void_tag(self):
        element = ptml.Input(name="test")
        self.assertEqual(str(element), '<input name="test"/>')

    def test_dashed_attribute(self):
        element = ptml.Div(data_testname="dashed")
        self.assertEqual(str(element), '<div data-testname="dashed"></div>')

    def test_reserved_name_attribute(self):
        element = ptml.Input(id_="id-test", type_="text", class_="mdc-inputfield")
        self.assertEqual(str(element), '<input id="id-test" type="text" class="mdc-inputfield"/>')

    def test_none_attribute(self):
        element = ptml.Div(id_=None)
        self.assertEqual(str(element), '<div></div>')

    def test_conditional_classlist_attribute(self):
        element = ptml.Div(class_={'included_1': True, 'included_2': True, 'excluded': False})
        self.assertEqual(str(element), '<div class="included_1 included_2"></div>')

    def test_conditional_empty_attribute(self):
        element = ptml.Div(data_test={'excluded': False})
        self.assertEqual(str(element), '<div></div>')

    def test_true_boolean_attribute(self):
        element = ptml.Input(type_="checkbox", checked=True)
        self.assertEqual(str(element), '<input type="checkbox" checked/>')

    def test_false_boolean_attribute(self):
        element = ptml.Input(type_="checkbox", checked=False)
        self.assertEqual(str(element), '<input type="checkbox"/>')

    def test_attribute_content_escaped(self):
        element = ptml.Div(data_test='''"><script>alert('Hello');</script>''')
        self.assertEqual(
            str(element),
            '<div data-test="&quot;&gt;&lt;script&gt;alert(&#39;Hello&#39;);&lt;/script&gt;"></div>')
    
    def test_body_elements(self):
        element = ptml.Div() / [
            ptml.I(class_="material-icons") / ["edit"],
            ptml.I(class_="material-icons") / ["person"]
        ]
        self.assertEqual(
            str(element),
            '<div><i class="material-icons">edit</i><i class="material-icons">person</i></div>')

    def test_element_body_escaped(self):
        element = ptml.Div() / ['''<script>alert('Hello');</script>''']
        self.assertEqual(
            str(element), 
            '<div>&lt;script&gt;alert(&#39;Hello&#39;);&lt;/script&gt;</div>')
