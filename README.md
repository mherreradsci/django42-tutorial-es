# Django 4.2 LTS Tutorial en Español

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg) ![Coverage][def]

El objetivo de este repositorio es proponer una forma para hacer un proyecto Django abarcando el ciclo de vida completo. Es decir, desde cero hasta Producción.

![Screenshot from 2023-07-10 00-23-54-900xX](https://github.com/mherreradsci/django42-tutorial-es/assets/73266769/acd34935-5b99-4fc9-95f1-1e8489361b1e)





## Pendientes:

* Form validation
* Testing
* Moldelo (n2n, geo, etc)
* CI/CD (pipelines)
* Contribución (How to)
* Internacionalización y localización
* Deploy

## Etapa actual (Stage 25)
* Carga inicial de datos para modelos

## Siguiente etapa (Stage 26)
* Testing básico

## Documentación en español Diango 4.2
- [Documentación](https://docs.djangoproject.com/es/4.2/)
- [Tutorial Django](https://docs.djangoproject.com/es/4.2/intro/tutorial01/)
- [Instrucciones detalladas de para instalar Django 4.2 (Ingles)](https://github.com/django/django/blob/9d756afb07de8ef6e4d1980413979496643f1c3b/docs/intro/install.txt)

## Propuesta de desarrollo
La propuesta de desarrollo es crecer en capítulos que se implementaran con branches de git con la nomenclatura NN-Inicio .... NN-Termino

## Requerimientos
- Django versión 4.2 LTS
- Python 3.8  (Python 3.8 es la versión mínima para Django 4.2)

## Ambiente para desarrollo
- Ubuntu 18.04
- Visual Studio Code Versión 1.77.0

## Preparar ambiente (linux)
### Crear directorio base y fuentes para el proyecto, por ejemplo:
```
$ mkdir -p ~/Proyectos/d42_proj/src
$ cd ~/Proyectos/d42_proj
```
### Clonar este repo
```
$ git clone https://github.com/mherreradsci/django42-tutorial-es.git ./src
```

### Instalación
```
$ cd ~/Proyectos/d42_proj
$ python3.8 -m venv ve_py38_django42
$ source ve_py38_django42/bin/activate

$ (ve_py38_django42) python --version
Python 3.8.0

# Para eliminar el venv (solo si deseas volver a crear el ambiente)
(ve_py38_django42) deactivate # Cierra el ambiente virtual
$ rm -rf ./ve_py38_django42 # Elimina el directorio completo, es decir, el ambiente virtual

# Actualiza la versión de pip
(ve_py38_django42)$ python -m pip install pip --upgrade

# Instalar requerimientos
(ve_py38_django42)$ cd src
(ve_py38_django42)$ pip install -r requirements-dev.txt
```
## Ejecución
### Activar el ambiente virtual python y ejecutar el server (solo si está desactivado)
``` bash
$ source ve_py38_django42/bin/activate
```
### Migración inicial (crea una base de datos sqlite3)
```
(ve_py38_django42)$ python manage.py migrate
```
## Carga inicial de datos
### Crear usuario para carga inicial
* Debe reemplazar \<clave\> por su propia clave

```
(ve_py38_django42)$ echo "from accounts.models import User; User.objects.create_superuser('init', '', '<clave>')" | python manage.py shell
```

### Carga datos para lookup tables. En este caso, para MAC_ADDRESS_TYPES
```
(ve_py38_django42)$ python manage.py loaddata init_mac_address_types.json
```
### Carga datos para Customers, devices y MAC Address
```
(ve_py38_django42)$ python manage.py loaddata init_customers.json
(ve_py38_django42)$ python manage.py loaddata init_devices.json
(ve_py38_django42)$ python manage.py loaddata init_mac_addresses.json
```

### Ejecutar el servidor de desarrollo
```
(ve_py38_django42)$ python manage.py runserver
```
#### Por omisión, el server se ejecuta en el puerto 8000 en el local host
http://127.0.0.1:8000/

#### Para terminar el server, desde la consola python
```
<CTRL+C>
```
### Desactivar el ambiente virtual python
```
(ve_py38_django42)$ deactivate
```

## Referencias
### Try Django 3.2 - Python Web Development Tutorial Series
CodingEntrepreneurs
https://youtube.com/playlist?list=PLEsfXFp6DpzRMby_cSoWTFw8zaMdTEXgL


[def]: https://img.shields.io/badge/Coverage-99%25-brightgreen.svg
