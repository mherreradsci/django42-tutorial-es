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
        # default=8, # "NONAME",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_updated_by",
        related_query_name="%(app_label)s_%(class)ss",
        # default=8, # "NONAME",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
