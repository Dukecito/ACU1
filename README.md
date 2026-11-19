# ACU1 - Ciberseguridad

Base inicial del proyecto Django. El entorno de esta fase usa SQLite local; no
configura ni debe conectarse a una base de datos de producción.

## Requisitos

- Python 3.14.7
- Git

## Instalación en Windows (PowerShell)

Comprueba primero que `py -3.14 --version` informa exactamente `Python 3.14.7`.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Si la política de PowerShell impide activar scripts, usa `cmd.exe` y ejecuta
`.venv\Scripts\activate.bat`, o invoca directamente
`.venv\Scripts\python.exe` en los comandos siguientes.

Genera una clave local y asígnala a `DJANGO_SECRET_KEY` en `.env`. Mantén la
misma clave entre reinicios y no la compartas ni la subas a Git:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

`.env` está excluido de Git. No reutilices claves ni contraseñas de otros
entornos. El proyecto exige `DJANGO_SECRET_KEY` en todos los entornos y usa
español de Colombia (`es-co`) y la zona horaria `America/Bogota`.

## Comprobación y servidor local

```powershell
python manage.py check
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. La página inicial de Django puede mostrar un 404
hasta que se autoricen y agreguen rutas de la aplicación.

## Modelos iniciales

La app `ciberseguridad` contiene los modelos del código aprobado y su migración
inicial. La migración no se aplica automáticamente. Antes de integrar con
SAIUNISARC, verifica las entidades institucionales equivalentes para evitar
duplicar tablas existentes.

## Estructura inicial de la app (D01-SDEV)

La app existente se completa con estos archivos:

- `ciberseguridad/urls.py`: declara el espacio de nombres de la app y deja
  la lista de rutas vacia hasta definir las pantallas.
- `ciberseguridad/templates/ciberseguridad/base.html`: plantilla base con
  bloques de titulo y contenido para las pantallas posteriores.

Las notas D01-SDEV en ambos archivos explican el motivo de estos cambios.
Django ya tiene registrada la app y habilitada la busqueda de sus plantillas
mediante `APP_DIRS=True`.

Se propone `/ciberseguridad/` como prefijo de integracion, pendiente de
acordar con Diego. Por eso, `config/urls.py` conserva sus rutas actuales y
todavia no incluye las rutas de esta app. Esta estructura no agrega una
pagina de inicio ni formularios; la navegacion se define en D02-SDEV.

### Responsabilidad y fuentes revisadas

Esta tarea corresponde a Santiago Duque en desarrollo (D01-SDEV, 3 horas
planeadas). Su función de soporte tiene una tarjeta separada (D01-SSOP,
1 hora planeada) para versiones, dependencias y variables de entorno.
Estas estimaciones no son horas reales registradas.

Se contrastaron el plan, el documento de responsabilidades, el control del
proyecto y los formularios entregados en `Actualizacion Planeación.zip`,
junto con `UNISARC_Formularios_Ciberseguridad.xlsx`.

El Excel de formularios recibido ya contiene 96 encabezados entre F-GTI-01
y F-GTI-09. F-GTI-03 tiene 13 campos e incluye `Area Afectada` en L1. La
planificación lo describe como 12 originales más uno adicional; se debe
aclarar esa diferencia de versión con Chirley y Diego antes de implementar
F03, conservando un solo campo de área afectada. Su relación propuesta con
`EstructuraOrganica` sigue pendiente de validación técnica.

El diseño del menú, las rutas F01-F09 y la revisión de autenticación se
trabajan en D02-SDEV. Los modelos, validadores y migraciones de D03-SDEV se
coordinan con Diego. La plantilla de D01 es únicamente una estructura base.

## Verificación inicial de soporte (D01-SSOP)

El [checklist de instalación inicial](docs/soporte/D01-SSOP-checklist.md)
registra versiones, variables de entorno sin claves y los pasos para
reproducir la preparación local. Las comprobaciones registradas corresponden
al entorno de Santiago; PostgreSQL de pruebas se trabaja en D02-SSOP.
