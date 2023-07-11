from backports.zoneinfo import ZoneInfo
from django.utils import timezone
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AuditInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_created_by",
        related_query_name="%(app_label)s_%(class)ss",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_updated_by",
        related_query_name="%(app_label)s_%(class)ss",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class ValidityInfo(AuditInfo):
    active_from = models.DateTimeField(blank=True, null=True, default=timezone.now)
    active_until = models.DateTimeField(
        blank=True,
        null=False,
        default=timezone.datetime(
            year=2501,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=ZoneInfo("UTC"),
        ),
    )
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
