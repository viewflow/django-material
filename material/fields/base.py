from ...html_factory import Part


def attrs(*attributes):
    """Join all not None attributes."""
    return ' '.join(attr for attr in attributes if attr is not None)


def attr(attr, cond=True, required=False):
    """Shortcut for attribute definition.

    During render, all None attributes is skipped, and not included
    into html output.

    Depends on `cond` value, attribute would be ignored, or set to ""
    if attribute is required

    >>> attr("example")
    "example"
    >>> attr("example", cond=False)
    None
    >>> attr("example", cond=False, required=True)
    ""
    >>> attr(None)
    None
    >>> attr(None, required=True)
    ""

    """
    value = attr if attr is not None else ""
    return value if bool(cond) else ("" if required else None)


class ControlWrapper(object):
    pass


class PartHelpText(Part):
    def __init__(self, bound_field):
        super(PartHelpText, self).__init__(bound_field, name="help_text")


class PartErrors(Part):
    def __init__(self, bound_field):
        super(PartErrors, self).__init__(bound_field, name="errors")


class PartHiddenInitial(Part):
    def __init__(self, bound_field):
        super(PartHiddenInitial, self).__init__(bound_field, name="hidden_initial")
