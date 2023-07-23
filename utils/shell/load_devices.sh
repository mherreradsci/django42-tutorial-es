#!/bin/bash

# Elimina y Crea 50 registros de devices con código 'CD<NNNN>' y nombre "Device <NNNN>"
# Observación: Este script elimina los devices que tienen el "pattern" 'CD<NNNN>'
# Para ejecutar:
#   En un bash shell, dentro del virtua environment python y en el directorio
#   base del proyecto (./src)
#   (ve_py38_django42)$ bash ./utils/shell/load_devices.sh
#
# Probado con BD SQLite
# Documentación:
# # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create

python manage.py shell << EOF
from devices.models import Device
from django.utils import timezone
from accounts.models import User


Device.objects.filter(code__iregex=r"^CD[0-9]{4,}$").delete()

user = User.objects.get(username='init')

# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
Device.objects.bulk_create(
    [
        Device(
            code="CD" + str(id).zfill(4),
            name="Device " + str(id).zfill(4),
            created_by=user,
            created_at=timezone.now(),
            updated_by=user,
            updated_at=timezone.now(),
        )
        for id in range(1, 51)
    ]
)
exit()
EOF

# Control
test $? -eq 0 && echo "SUCCESS: El comando anterior fue ejecutado con éxito" && exit 0
