# Informe técnico — D02-DEV

**Actividad:** diseño lógico y borradores para el ciclo de incidentes
**Tiempo planificado:** 4 horas
**Estado:** entregables de diseño preparados para revisión. No se registró aquí
el tiempo real empleado.

## 1. Auditoría del repositorio

- Rama revisada: `main`, commit `e754a51` (`+App ciberseguridad +Modelo`),
  sin comprobar el estado remoto en esta revisión (no se hizo fetch ni push).
- `ciberseguridad/models.py` define 11 modelos: `Estado`, `Ciudad`,
  `EstructuraOrganica`, `Sede`, `Cargo`, `Tipodoc`, `Persona`,
  `FuncionarioCargo`, `TipoVinculacion`, `PersonaVinculacion` y `TipoVisita`.
  No contiene entidades de incidentes.
- `ciberseguridad/migrations/0001_initial.py` crea esos mismos 11 modelos.
  No se encontraron modelos de los formularios F-GTI-01 a F-GTI-07 en esa
  migración.
- El código de referencia `modelo_gral.docx` contiene las entidades
  institucionales compartidas. El plan indica que `Persona`, `Cargo`,
  `EstructuraOrganica`, `Sede` y otras listas existentes deben reutilizarse,
  no recrearse.
- `Estado` corresponde al departamento geográfico relacionado con `Ciudad`;
  no representa el estado operativo de un incidente.
- La app está registrada en `config/settings.py`. Por tanto, las copias
  actuales son modelos Django activos en el código de ACU1, aunque todavía no
  estén creadas en la base local.
- En el [`models.py`](../../ciberseguridad/models.py) actual, `Persona.user` es
  un `CharField` (línea 355); no hay una FK
  demostrada a `auth.User`. La ubicación real de los modelos y la relación de
  identidad deben verificarse en el repositorio completo de SAIUNISARC.

### Evidencia por modelo

| Modelo local | Declaración en `models.py` | `CreateModel` en `0001_initial.py` |
|---|---:|---:|
| Estado | 4 | 16 |
| Ciudad | 15 | 59 |
| EstructuraOrganica | 32 | 72 |
| Sede | 107 | 159 |
| Cargo | 163 | 92 |
| Tipodoc | 226 | 23 |
| Persona | 242 | 111 |
| FuncionarioCargo | 377 | 141 |
| TipoVinculacion | 416 | 35 |
| PersonaVinculacion | 434 | 184 |
| TipoVisita | 456 | 47 |

Referencias: [`0001_initial.py`](../../ciberseguridad/migrations/0001_initial.py)
y registro en [`settings.py`](../../config/settings.py), línea 52.

### Riesgo de duplicación

**Alto.** Si se aplicara `0001_initial.py` en la base compartida o integrada,
Django intentaría crear tablas locales para los 11 modelos institucionales.
Aunque los nombres físicos de tabla no coincidan con los de SAIUNISARC, habría
dos fuentes de verdad para personas, cargos, sedes, áreas y catálogos. Esto
podría producir registros divergentes y relaciones incompatibles. No se
modificaron ni eliminaron esos modelos o la migración.

El diagrama trata esos modelos como referencias externas hasta comprobar su
`app_label`, nombres de tabla, PK, migraciones y compatibilidad en SAIUNISARC.

## 2. Estado local de migraciones

Consulta no destructiva, sin ejecutar `migrate`:

- `manage.py showmigrations ciberseguridad`: `0001_initial` aparece sin marcar
  (`[ ]`).
- `manage.py showmigrations --plan`: todas las migraciones listadas aparecen
  sin marcar.
- `db.sqlite3` existe localmente, pero tiene **0 bytes** y una lectura SQLite
  en modo solo lectura no encontró tablas, incluida `django_migrations`.

**Conclusión:** no hay evidencia de migraciones aplicadas en esta base local.
Esto no permite inferir el estado de otra base ni de producción; no se accedió a
ninguna base externa.

## 3. Diseño entregado

- [Diagrama, cardinalidades y PK/FK](01-esquema-logico-incidentes.md).
- [Borrador de modelos, campos F-GTI y tipos](02-borrador-modelos-django.md).
- Las etapas de F-GTI-02 a F-GTI-07 se vinculan al mismo incidente. F-GTI-04
  tiene múltiples acciones; F-GTI-07 se separa en una lección y múltiples
  acciones de mejora con estado independiente.
- Se propone que criticidad en F-GTI-03 y usuarios afectados en F-GTI-06 sean
  datos derivados de F-GTI-02, no copias almacenadas.
- F-GTI-08 y F-GTI-09 quedan como consultas/reportes, no como entidades de
  captura en este alcance.

## 4. Riesgos, dudas y decisiones del equipo

1. **Ubicación institucional:** identificar el repositorio/app real de
   SAIUNISARC y comprobar si los 11 modelos del código local son copias.
2. **Identidad:** determinar cómo se relacionan usuarios autenticados y
   `Persona`; `Persona.user` es texto en el fragmento disponible.
3. **Cardinalidades:** confirmar si clasificación, investigación, recuperación,
   cierre y lección son únicos por incidente o si se necesita historial.
   Recuperación podría requerir varias filas si se restablecen varios servicios.
4. **Catálogos:** aprobar clasificación, origen, impacto CIA y estados de
   acciones. El SLA enumera Bajo, Medio, Alto y Crítico; los estados de F-GTI-04
   y F-GTI-07 no están especificados. El catálogo geográfico `Estado` no debe
   usarse como flujo del incidente.
5. **Áreas:** validar `Area Afectada` de F-GTI-03 como FK a
   `EstructuraOrganica`, distinta de la Dependencia reportante y el Area
   Responsable.
6. **Aprobación de cierre:** definir quién autoriza, cómo se registra la
   autorización, quién puede reabrir y cómo se conserva cada cierre.
7. **Fechas/duración:** F-GTI-06 incluye `Tiempo Indisponibilidad`, pero las
   fuentes no establecen de forma completa los instantes de caída y
   restablecimiento. No calcular si faltan datos.
8. **Evidencias:** decidir si un formulario puede tener varios archivos y
   aprobar almacenamiento privado, límites de tamaño/extensión, retención y
   auditoría.
9. **Integridad histórica:** acordar `on_delete` y tratamiento de cambios o
   inactivación de Persona, Cargo, Sede y EstructuraOrganica sin perder
   incidentes.
10. **Código único:** confirmar formato de `No Incidente` y mecanismo concurrente
    de generación; no reutilizar el campo `Ticket` de la mesa de ayuda.
11. **Datos monetarios y longitudes:** aprobar precisión/escala de `Costo Total`
    y longitudes máximas no definidas en las fuentes.
12. **Campos derivados:** confirmar si se guardan instantáneas de la
    Dependencia/Cargo reportante o si se consultan los valores institucionales
    actuales.

## 5. Evidencia y límites de la actividad

Se revisaron `models.py`, `0001_initial.py`, `config/settings.py`, el historial
local de migraciones y `db.sqlite3` en modo de solo lectura. En la revisión del 11/11/2026 se contrastó el
diseño con los archivos locales `04_Formularios_FGTI_ACTUALIZADOS.docx`,
`01_Plan_Ciberseguridad_15_Dias_ACTUALIZADO.docx` y las hojas `MODELOS UNISARC`,
`CAMPOS F-GTI`, `REQUISITOS RF`, `REQUISITOS RNF` y `SLA UNISARC` del Excel de
control.

No se modificaron `models.py` ni migraciones; no se crearon ni activaron modelos
de incidentes, no se generó otra migración, no se ejecutó `migrate`, no se
conectó a producción y no se hizo commit ni push. La aprobación del equipo sigue
siendo necesaria antes de implementar el esquema.


## 6. Verificación de entrega del 11/11/2026

- `python manage.py check`: sin errores (0 silenciados), con el entorno .venv local.
- Lectura de db.sqlite3: 0 bytes y ninguna tabla; no se ejecutó migrate.
- 04-trazabilidad-campos.csv cubre 96 filas únicas: F01=13, F02=12,
  F03=13, F04=8, F05=9, F06=9, F07=13, F08=8 y F09=11.
- Los 96 campos corresponden al catálogo del control, que refiere 95 originales
  y el campo adicional Área afectada. No equivalen a 96 columnas de base de datos.
- Se preparó 05-revision-equipo-D02-DEV.md para registrar decisiones reales.
- No se verificó el libro original UNISARC ni modelo_gral como archivos
  independientes; los Word actualizados y el control contienen sus referencias.
- Diferencias entre fuentes: los Word definen Evitar recurrencia como texto;
  el control sugiere sí/no. Los Word definen duración para Tiempo Indisponibilidad;
  el control contiene una sugerencia genérica de texto. El control propone
  DecimalField(12,2) para Costo Total y modelo vinculado para Evidencias.
  Se conservan propuestas explícitas, sin presentarlas como acuerdos aprobados.
- RF-01 figura asignado a D02-DEV en el plan, aunque la tarjeta pide diseño.
  El acceso institucional no está implementado ni verificado. Aclarar esta
  discrepancia con planificación antes de considerar cumplido RF-01.

Resultado: diseño preparado y comprobado documentalmente; aceptación de las
relaciones por el equipo, registro de horas reales y publicación en Trello pendientes.
