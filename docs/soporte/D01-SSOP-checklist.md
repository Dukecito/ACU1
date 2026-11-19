# Checklist de instalación inicial

Proyecto: ACU1 - Ciberseguridad UNISARC

Actividad: D01-SSOP - Verificar entorno local

Responsable: Santiago Duque - Support Manager

Verificación local: 11 de noviembre de 2026

Tiempo planeado: 1 hora. Tiempo real: pendiente de informar.

La entrega reúne los requisitos y las comprobaciones del entorno para que
otro integrante pueda preparar una copia local del proyecto.

## Versiones observadas

| Componente | Versión |
| --- | --- |
| Python | 3.14.7 |
| Django | 5.2.19 |
| pip | 26.2.1 |
| Git | 2.55.0.windows.5 |
| asgiref | 3.13.0 |
| pillow | 13.0.0 |
| python-dotenv | 1.2.4 |
| sqlparse | 0.6.1 |
| tzdata | 2026.6 |

Las seis dependencias del proyecto respetan requirements.txt. Python, pip
y Git se registran como herramientas del entorno.

## Checklist verificado

| Comprobación | Estado | Evidencia |
| --- | --- | --- |
| Entorno virtual | Verificado | .venv usa Python 3.14.7 y está seleccionado en VS Code. |
| Dependencias | Verificado | pip check: No broken requirements found. |
| Configuración Django | Verificado | manage.py check: System check identified no issues (0 silenced). |
| Plantilla y rutas base | Verificado | base.html cargó y se renderizó; urls.py tiene sintaxis válida. |
| Variables privadas | Verificado | .env y .venv están excluidos de Git. La clave en .env.example está vacía. |

Las comprobaciones de Django, dependencias y plantilla se ejecutaron
durante la instalación del entorno. Las versiones, el README y el archivo
de ejemplo se contrastaron al preparar esta entrega.

## Variables de entorno

| Variable | Uso local |
| --- | --- |
| DJANGO_SECRET_KEY | Clave privada y persistente de Django. Cada equipo genera la suya; no se adjunta ni se sube a Git. |
| DJANGO_DEBUG | True en este entorno local de desarrollo. |
| DJANGO_ALLOWED_HOSTS | 127.0.0.1,localhost,testserver para las comprobaciones locales. |

.env.example conserva DJANGO_SECRET_KEY vacío. La clave local no forma
parte de esta evidencia.

## Instalación en otro equipo

### 1. Abrir una copia del proyecto

Instalar Python 3.14.7 y Git. Abrir la carpeta ACU1, donde están manage.py y requirements.txt. Comprobar la versión exacta antes de crear el entorno.

```powershell
py -3.14 --version
git --version
```

### 2. Crear el entorno

En un equipo nuevo, ejecutar desde la carpeta del proyecto:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe --version
```

### 3. Instalar las dependencias

Usar el intérprete de .venv evita depender de la activación de PowerShell.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Preparar las variables locales

Copiar el ejemplo solo si .env todavía no existe. Generar una clave propia y copiarla al valor DJANGO_SECRET_KEY de .env. Conservar esa clave entre reinicios y no compartirla.

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 5. Elegir el intérprete en VS Code

Abrir Python: Select Interpreter y seleccionar .venv\Scripts\python.exe. La barra de estado debe mostrar .venv (3.14.7).

### 6. Comprobar la instalación

Confirmar que Django carga, que las dependencias son compatibles y que la configuración del proyecto no presenta problemas.

```powershell
.\.venv\Scripts\python.exe -m django --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py check
```

## Resultado y pendientes

El entorno local quedó verificado con Python 3.14.7 y Django 5.2.19. No se
aplicaron migraciones. La configuración actual usa SQLite local; PostgreSQL
de pruebas corresponde a D02-SSOP. Esta entrega no acredita el flujo de
formularios, la integración institucional ni una instalación en otro equipo.

El entorno provisional de Python 3.13 se conservó como respaldo fuera del
repositorio y se reemplazó por el de la versión solicitada.

Para cerrar la tarjeta faltan adjuntar la evidencia revisada, registrar el
tiempo real y recibir la revisión de Manuela. La hora indicada es planeada.

## Referencias

- Tarjeta D01-SSOP: https://trello.com/c/lmOH6L8n
- README.md, requirements.txt, .env.example y configuración local de ACU1.
- Resultados de pip check, manage.py check, compilación de urls.py y carga y
  renderizado de ciberseguridad/base.html obtenidos en el entorno local.
