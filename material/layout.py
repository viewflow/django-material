from material.ptml import Div, H3
from material.renderers import get_field_renderer


class _Auto(object):
    def __repr__(self):
        return 'AUTO'

    def __str__(self):
        return 'AUTO'


AUTO = _Auto()


def _convert_to_children(elements):
    result = []
    for element in elements:
        if isinstance(element, LayoutNode):
            result.append(element)
        elif isinstance(element, str):
            result.append(Field(element))
        else:
            raise ValueError(
                "Unknown element {} type {}".format(element, type(element)))
    return result


def _children_sizes(spans, grid_size=12, grid_name='desktop', keep_in_row=True):
    bound = sum(span for span in spans if span != AUTO)
    auto_count = sum(1 for span in spans if span == AUTO)

    if bound == 0 and not keep_in_row:
        # If children AUTO-sized - put every child on the own row
        return [grid_size for _ in spans]
    else:
        rest = grid_size - bound
        if rest <= 0 or grid_size % auto_count != 0:
            raise ValueError("Can't spead {} over {} columns on a {} grid".format(
                spans, grid_size, grid_name))
        return [
            rest // auto_count if child == AUTO else child
            for child in spans
        ]


class LayoutNode(object):
    """Base class for self-rendered nodes."""

    def __init__(self, desktop=AUTO, tablet=AUTO, mobile=AUTO):
        assert desktop == AUTO or 1 <= desktop <= 12
        self.desktop = desktop

        assert tablet == AUTO or 1 <= tablet <= 8
        self.tablet = tablet

        assert mobile == AUTO or 1 <= mobile <= 4
        self.mobile = mobile

    def render(self, form):
        raise NotImplementedError("Subclass should override this")


class Column(LayoutNode):
    """Place elements vertically stacked, one under another.

    Example:
        layout = Layout(
            Row(
                Column('first_name', 'last_name', desktop=8, tablet=6)
                'sex_options'
            )
        )
    """

    def __init__(self, *elements, **kwargs):
        self.id_ = kwargs.pop('id_', None)
        self.children = _convert_to_children(elements)
        super().__init__(**kwargs)

    def render(self, form):
        return Div(class_="dmc-form-column mdc-layout-grid__cell mdc-layout-grid__cell--span-12", id_=self.id_) / [
            child.render(form) for child in self.children
        ]


class Row(LayoutNode):
    """Spread elements over a single line.

    Example:

        layout = Layout(
            Row(
                'first_name',
                Row('last_name', 'sex', tablet=5)
            )
        )
    """

    def __init__(self,  *elements, **kwargs):
        self.id_ = kwargs.pop('id_', None)
        self.children = _convert_to_children(elements)
        super().__init__(**kwargs)

    def render(self, form):
        desktop = _children_sizes(
            [child.desktop for child in self.children], grid_size=12,
            grid_name='desktop', keep_in_row=True
        )
        tablet = _children_sizes(
            [child.tablet for child in self.children], grid_size=8,
            grid_name='tablet', keep_in_row=False
        )
        mobile = _children_sizes(
            [child.mobile for child in self.children], grid_size=4,
            grid_name='mobile', keep_in_row=False
        )

        def render_child(child, desktop, tablet, mobile):
            classes = ' '.join([
                "mdc-layout-grid__cell",
                "mdc-layout-grid__cell--span-{}-desktop".format(desktop),
                "mdc-layout-grid__cell--span-{}-tablet".format(tablet),
                "mdc-layout-grid__cell--span-{}-mobile".format(mobile)
            ])
            element = Div(class_=classes) / [
                child.render(form)
            ]
            return str(element)

        return Div(class_="dmc-form-row mdc-layout-grid__inner", id_=self.id_) / [
            render_child(*child_data)
            for child_data in zip(self.children, desktop, tablet, mobile)
        ]


class Fieldset(Column):
    def __init__(self,  title, *elements, **kwargs):
        self.title = title
        super().__init__(*elements, **kwargs)

    def render(self, form):
        element = Div(class_="dmc-form__formset") / [
            H3(class_="mdc-typography--subheading2") / [self.title],
            super().render(form)
        ]
        return str(element)


class Span(LayoutNode):
    """Span a form field over several columns.

    Example::
        layout = Layout(
            Row(Span('first_name'), Span('last_name'))
            Row(
                Span('email', tablet=6, mobile=3),
                'sex'
            )
        )

    By default span is auto-sized. On a desktop all auto-sized elements
    would be spread equally over the free place of a row, non occupied by
    elements with specific sizes.

    On mobile and tablet if all elements in a row have auto-sizes,
    each element would be plased in a new line. If even one element
    in a row has a specific size, all auto-sized elements would be
    keeped in a single line, like on a desktop.

    """
    def __init__(self, field_name, **kwargs):
        self.field_name = field_name
        super().__init__(**kwargs)

    def __str__(self):
        return 'Field {self.field_name} <{self.desktop}, {self.tablet}, {self.mobile}>'.format(self)

    def render(self, form):
        try:
            bound_field = form[self.field_name]
        except KeyError as exc:
            raise ValueError(
                '{} field not found in the {}'.format(self.field_name, type(form).__name__)
            ) from exc

        renderer_class = get_field_renderer(bound_field.field)
        renderer = renderer_class(bound_field)
        return str(renderer)


class Field(Span):
    def render(self, form):
        element = Div(class_="mdc-layout-grid__cell mdc-layout-grid__cell--span-12") / [
            super().render(form)
        ]

        return str(element)


class Layout(Column):
    """Form layout specification.

    Can be used in conjunction with  `{% material %}` template tag

    Example::

        layout = Layout(
            Row('first_name', 'last_name'),
            'email'
        )

        {% material form layout %}

    Each element of a layout could be spread over a several
    columns of the grid. The grid has 12 columns in desktop
    mode (>= 840px), 8 columns in tablet mode (>= 480px), and
    4 columns in phone mode (< 480px).
    """
    def render(self, form):
        element = Div(class_="mdc-layout-grid__inner") / [
            super().render(form)
        ]

        return str(element)

    def __str__(self):
        return 'Layout [{} elements]'.format(len(self.children))
