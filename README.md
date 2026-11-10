# ACU1 - Ciberseguridad

Base inicial del proyecto Django. El entorno de esta fase usa SQLite local; no
configura ni debe conectarse a una base de datos de producción.

## Requisitos

- Python 3.14
- Git

## Instalación en Windows (PowerShell)

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
