from datetime import date

from django.db import models
from django.utils import timezone


class TemporalQuerySet(models.QuerySet):
    """Temporal manager for models with `from_date`/`to_date` fields."""

    def set(self, **kwargs):
        today = timezone.now().date()

        self.filter(
            from_date__lte=today,
            to_date__gt=today,
        ).update(to_date=today)

        self.filter(
            from_date=today,
            to_date=today,
        ).delete()

        return self.create(
            from_date=today,
            to_date=date(9999, 1, 1),
            **kwargs
        )

    def current(self):
        today = timezone.now().date()

        return self.filter(
            from_date__lte=today,
            to_date__gt=today,
        ).first()
