import datetime
import six
import decimal

from django.db import router
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models.deletion import Collector
from django.utils import formats, timezone
from django.utils.encoding import force_text


def get_deleted_objects(root):
    """Collect linked objects required to be deleted.

    And maps each one to the `detail` page link.
    """
    using = router.db_for_write(root)
    collector = Collector(using=using)
    collector.collect([root])

    def format_callback(obj):
        opts = obj._meta

        try:
            return reverse(
                '{}:{}_{}_details'.format(opts.app_label, opts.app_label, opts.model_name),
                args=[obj._get_pk_val()])
        except NoReverseMatch:
            return None

    to_delete = collector.nested(format_callback)
    return to_delete


def format_value(value, empty_value_display):
    if value is None or value == "":
        return empty_value_display
    elif isinstance(value, datetime.datetime):
        return formats.localize(timezone.template_localtime(value))
    elif isinstance(value, (datetime.date, datetime.time)):
        return formats.localize(value)
    elif isinstance(value, six.integer_types + (decimal.Decimal, float)):
        return formats.number_format(value)
    elif isinstance(value, (list, tuple)):
        return ', '.join(force_text(v) for v in value)
    else:
        return force_text(value)
