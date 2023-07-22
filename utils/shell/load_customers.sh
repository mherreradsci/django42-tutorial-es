#!/bin/bash

# Elimina y Crea 50 registros de Customers con código 'CR<NNNN>' y nombre "Cliente <NNNN>"
# Observación: Este script elimina los customers que tienen el "pattern" 'CR<NNNN>'
# Para ejecutar:
#   En un bash shell, dentro del virtua environment python y en el directorio
#   base del proyecto (./src)
#   (ve_py38_django42)$ bash ./utils/shell/load_customers.sh
#
# Probado con BD SQLite
# Documentación:
# # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create

python manage.py shell << EOF
from customers.models import Customer
from django.utils import timezone
from accounts.models import User

user = User.objects.get(username='init')

Customer.objects.filter(code__iregex=r'^CR[0-9]{4,}$').delete()

Customer.objects.bulk_create(
    [
        Customer(
            code="CR" + str(id).zfill(4),
            name="Cliente " + str(id).zfill(4),
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
