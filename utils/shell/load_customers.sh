python manage.py shell << EOF
from customers.models import Customer
from django.utils import timezone

Customer.objects.filter(code__iregex=r'^CR[0-9]{4,}$').delete()

Customer.objects.bulk_create(
    [
        Customer(
            code="CR" + str(id).zfill(4),
            name="Cliente " + str(id).zfill(4),
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        for id in range(1, 51)
    ]
)
exit()
EOF
