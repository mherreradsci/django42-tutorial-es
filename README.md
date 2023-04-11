# Django 4.2 LTS Tutorial en Español
El objetivo de este repositorio es proponer una forma para hacer un proyecto Django abarcando el ciclo de vida completo. Es decir, desde cero hasta Producción

## Propuesta de desarrollo
La propuesta de desarrollo es crecer en capítulos que se implementaran con branches de git con la nomenclatura NN-Inicio .... NN-Termino

## Requerimientos
- Django versión 4.2 LTS
- Python 3.8  (Python 3.8 es la versión mínima para Django 4.2)

## Ambiente para desarrollo
- Ubuntu 18.04
- Visual Studio Code Versión 1.77.0

## Instalación
```
$ python3.8 -m venv ve_py38_django42
$ source ve_py38_django42/bin/activate

$ (ve_py38_django42) python --version
Python 3.8.0

# Para eliminar el venv (solo si deseas volver a crear el ambiente)
(ve_py38_django42) deactivate # Cierra el ambiente virtual
$ rm -rf ./ve_py38_django42 # Elimina el directorio completo, es decir, el ambiente virtual

# Actualiza la versión de pip
$ python -m pip install pip --upgrade

$ pip install -r requirements.txt
```
## Ejecución
### Activar el ambiente virtual python y ejecutar el server
``` bash
$ source ve_py38_django42/bin/activate

(ve_py38_django42)$ python manage.py runserver
```
#### El server se ejecuta en
http://127.0.0.1:8000/

### Desactivar el ambiente virtual python
```
(ve_py38_django42)$ deactivate
$
```
