from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

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

    # def save(self, *args, **kwargs):
    #     print("AuditInfo:save")
    #     print("AuditInfo:save:self.created_by:", self.created_by)
    #     print("AuditInfo:save:args:", args)
    #     print("AuditInfo:save:kwargs:", kwargs)

    #     user = kwargs.pop("user", None)
    #     print("AuditInfo:save:user:", user)

    #     if user:
    #         print("AuditInfo:save:self.pk", self.pk)
    #         if self.instance.pk:
    #             print("AuditInfo:save:self.pk:Update:Ok")
    #             # Object already exists
    #             self.updated_by = user  # This can be passed from maybe your views
    #         else:
    #             print("AuditInfo:save:self.pk:New:Ok")
    #             self.created_by = user  # This can be passed from maybe your views
    #             self.updated_by = user  # This can be passed from maybe your views
    #     super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ValidityInfo(AuditInfo):
    active_from = models.DateTimeField(blank=True, null=False, default=timezone.now)
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

    @property
    def active(self):
        "Returns if the instance if active or not."
        now = timezone.now()
        return self.active_from <= now and now <= self.active_until

    def clean(self):
        # Validate consistency in Active
        errors = {}

        if not self.active_from:
            errors.setdefault("active_from", []).append("active_from without value")

        if not self.active_until:
            errors.setdefault("active_until", []).append("active_until without value")
        if not errors:
            if self.active_from >= self.active_until:
                errors.setdefault("active_until", []).append(
                    _("active_until must be less or equal to active_from")
                )

        if len(errors) > 0:
            # raise errors
            raise ValidationError(errors)

    class Meta:
        abstract = True
