from django.db import models


# Create your models here.
class Customer(models.Model):
    code = models.CharField(unique=True, max_length=6, null=True, blank=False)
    name = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "customers"  # 'example"."customers'
