from django.db import models
from django.urls import reverse

from common.models import ValidityInfo


class Customer(ValidityInfo):
    code = models.CharField(unique=True, max_length=6, null=True, blank=False)
    name = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = "customer"
        verbose_name_plural = "customers"

        db_table = "customers"  # 'example"."customers'
        # db_table_comment = "Customers"
        # indexes = [
        #     models.Index(fields=["name"], name="customers_ix01"),
        # ]

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("customers:list")
