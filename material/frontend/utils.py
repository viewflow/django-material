from django.db import router
from django.db.models.deletion import Collector
from django.urls import NoReverseMatch, reverse


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
