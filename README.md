# Django 4.2 LTS Project
El objetivo de este repositorio es proponer una forma para hacer un proyecto Django abarcando el ciclo de vida completo. Es decir, desde cero y hasta Producción
## Propuesta de desarrollo
La propuesta de desarroloo es crecer en capitulos que se implementaran con branches de git con la nomenclatura cap_nn

## Requerimientos
Django versión 4.2 LTS
Python 3.8

## Ambiente para desarrollo
1) Ubuntu 18.04
2) Visual Studio Code Vrsión 1.77.0

## Instalación
```
$ python3.8 -m venv ve_py38_django42
$ source ve_py38_django42/bin/activate

$ (ve_py38_django42) python --version
Python 3.8.0

# Para eliminar el venv (solo si deseas volver a crear el ambiente)
(ve_py38_django42) deactivate # Cierra el ambiente virtual
$ rm -rf ./ve_py38_django42 # Elimina el directorio completo, es decir, el ambiente virtual

# Actualiza cersión de pip
$ python -m pip install pip --upgrade

$ pip install django==4.2
```

