python manage.py shell << EOF
from devices.models import Device
from django.utils import timezone
from accounts.models import User



Device.objects.filter(code__iregex=r"^CD[0-9]{4,}$").delete()

user = User.objects.get(username='dadmin')
Device.objects.bulk_create(
    [
        Device(
            code="CD" + str(id).zfill(4),
            name="Name " + str(id).zfill(4),
            created_by=user,
            created_at=timezone.now(),
            updated_by=user,
            updated_at=timezone.now(),
        )
        for id in range(1, 21)
    ]
)
exit()
EOF
