# D01-DEV — Diagnóstico de la base disponible

Proyecto: ACU1 — Ciberseguridad UNISARC.
Responsable: Diego Alejandro Carvajal Garzón.
Fecha de revisión: 13 de noviembre de 2026.

## Alcance

El código disponible en la carpeta de trabajo corresponde al repositorio ACU1. Es una base Django independiente; con los archivos revisados todavía no se puede demostrar que esté integrada al proyecto completo saiunisarc.

Este diagnóstico documenta lo que se pudo comprobar en ACU1 y lo que falta solicitar al responsable institucional. La inspección completa de saiunisarc permanece pendiente y está relacionada con el bloqueo B-01, que ya figura abierto en el control compartido.

## Archivos y componentes encontrados

| Archivo o carpeta | Función y hallazgo |
|---|---|
| manage.py | Punto de entrada de los comandos de Django. |
| config/settings.py | Configuración de apps, base de datos, autenticación incluida y ajustes regionales. Idioma es-co, zona horaria America/Bogota. |
| config/urls.py | Enrutamiento del proyecto. Actualmente declara la ruta admin/. |
| config/asgi.py y config/wsgi.py | Entradas del servidor Django. |
| ciberseguridad/apps.py | Configuración de la app, registrada en INSTALLED_APPS. |
| ciberseguridad/models.py | Contiene 11 modelos institucionales locales. No contiene todavía los modelos del ciclo de incidentes. |
| ciberseguridad/migrations/0001_initial.py | Define la creación de los modelos locales. Debe revisarse antes de integrar con una base institucional para evitar duplicar entidades. |
| ciberseguridad/views.py | Conserva la estructura inicial; no hay pantallas de incidentes implementadas aquí. |
| requirements.txt | Dependencias fijadas, entre ellas Django 5.2.19. |
| .env.example y .gitignore | Guía de variables y exclusiones del repositorio. No se incluyen valores secretos en este diagnóstico. |
| README.md | Instrucciones de instalación y arranque. Corregido localmente a Python 3.12 o superior; el comando usa py -3. El cambio todavía no se ha publicado en Git. |
| docs/arquitectura/ | Documentación del diseño de D02-DEV y matriz de campos. |

El último commit local revisado fue 9ab9b2751af2b37f50cb4718d061e87906d67b76, «+Documentacion de proyecto.». No se consultó ni actualizó el remoto durante esta preparación.

## Usuarios y relaciones

Los modelos locales son Estado, Ciudad, EstructuraOrganica, Sede, Cargo, Tipodoc, Persona, FuncionarioCargo, TipoVinculacion, PersonaVinculacion y TipoVisita.

Persona.user es un campo de texto; no prueba por sí mismo una relación FK con la cuenta de Django. FuncionarioCargo sí relaciona Persona y Cargo. Cargo se relaciona con EstructuraOrganica y Sede. Se necesita comprobar cómo resuelve la identidad y las asignaciones activas el sistema institucional completo.

Las apps y el middleware habituales de autenticación de Django están incluidos en la configuración. Esto no demuestra que el acceso institucional de saiunisarc esté conectado ni que el formulario de incidentes reconozca al funcionario.

## Base de datos y conexión institucional

La configuración disponible usa SQLite local. No se ha demostrado una conexión a PostgreSQL de pruebas ni una conexión con la base institucional. PostgreSQL de pruebas corresponde también a la actividad D02-SSOP y al bloqueo B-02 del control.

Antes de integrar hay que confirmar dónde están definidos los modelos institucionales y sus tablas. Los 11 modelos presentes en ACU1 pueden duplicar entidades que ya existen en saiunisarc; no se deben crear como una segunda fuente de datos sin revisar esa integración.

## Evidencia de funcionamiento

En su comentario de D01-DEV, Manuela informa que pudo instalar dependencias, probar la exigencia de .env, ejecutar migraciones y manage.py check, iniciar el servidor y comprobar la redirección de /admin/ al login. También confirma idioma, zona horaria y exclusión de archivos locales en Git.

Esos resultados se atribuyen a la revisión de QA y a su entorno de pruebas. En esta preparación no se ejecutaron migraciones ni se comprobó una conexión de producción.

El enlace inicial 4d6fafb no contiene todavía la corrección regional. La evidencia de esa corrección está en:

https://github.com/Dukecito/ACU1/commit/b34be199a655696085a3d339371b0407bd8db08a

## Pendientes para completar D01-DEV

1. Obtener acceso al repositorio institucional y confirmar la rama que se debe usar.
2. Identificar las apps, tablas y migraciones reales de Persona, Cargo, FuncionarioCargo, EstructuraOrganica y Sede.
3. Confirmar cómo se relaciona el usuario de sesión con Persona y cómo se consulta una asignación activa.
4. Acordar con Katerin si ACU1 continúa como base temporal mientras se resuelve B-01, o si el desarrollo debe trasladarse a una app dentro de saiunisarc.
5. Actualizar la evidencia de la tarjeta y el seguimiento del bloqueo cuando se autorice la publicación.

La base técnica disponible tiene resultados favorables de QA. La aceptación de D01-DEV sigue pendiente porque aún falta completar la inspección y aclarar el enfoque institucional. Este documento se entrega para revisión, sin declarar esas decisiones resueltas.


## Correcciones y comprobaciones del 13/11/2026

Se ajustó el README local para indicar Python 3.12 o superior y usar `py -3`
al crear el entorno. Las versiones instaladas de las seis dependencias declaran
compatibilidad con Python 3.12 en sus metadatos. QA reportó una prueba con 3.12;
la comprobación propia se hizo con el entorno local Python 3.14.

En esta revisión `manage.py check` terminó sin errores. Una petición de prueba
de Django a `/admin/` devolvió 302 hacia `/admin/login/?next=/admin/`. Esta
comprobación no requirió aplicar migraciones; db.sqlite3 seguía en 0 bytes.
La instalación y las migraciones que reportó Manuela corresponden a su entorno.

El tiempo de D01 fue confirmado por Diego: inicio 09/11/2026 a las 23:00,
fin 10/11/2026 a las 02:28 y pausa de 32 minutos. Tiempo efectivo: 176 minutos
(2 horas y 56 minutos). El registro se agregó una sola vez al control compartido.

B-01 permanece abierto. La disponibilidad del repositorio institucional y el
uso de ACU1 como base temporal todavía deben confirmarse con Katerin. No se
registra una aprobación que aún no ha ocurrido. Las correcciones locales están
sin commit ni push.
