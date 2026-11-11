# Borrador documental de modelos Django

**No ejecutable:** este documento no se importa desde Django, no activa modelos
y no genera migraciones. Los nombres `APP_INSTITUCIONAL.*` son marcadores: no se
ha comprobado el `app_label` real de los modelos en SAIUNISARC. Las longitudes,
opcionalidad y políticas de borrado no especificadas por la fuente requieren
validación antes de implementar.

## Entidades propuestas

### Incidente — F-GTI-01

`no_incidente` es el código de negocio único; `id` sería la PK técnica.

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `no_incidente` | `CharField(unique=True)` | Automático. Longitud y estrategia segura de consecutivo pendientes. No es el campo `Ticket`. |
| Fecha Reporte | `fecha_reporte` | `DateField` | La asigna la aplicación; confirmar si se puede editar. |
| Hora | `hora` | `TimeField` | La asigna la aplicación al crear el reporte. |
| Reportado por | `reportado_por` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Modelo institucional por verificar. |
| Cargo | `cargo` | `ForeignKey(APP_INSTITUCIONAL.Cargo)` | El documento indica que puede haber varios cargos; regla de selección pendiente. |
| Dependencia | `dependencia` | `ForeignKey(APP_INSTITUCIONAL.EstructuraOrganica)` | Derivada del cargo según la fuente; decidir si se almacena como instantánea. |
| Correo | `correo` | `EmailField` | Fuente sugerida: correo institucional de Persona. |
| Telefono | `telefono` | `CharField` | No usar un tipo numérico; longitud por confirmar. |
| Ubicacion | `ubicacion` | `ForeignKey(APP_INSTITUCIONAL.Sede)` | La fuente también requiere detalle del lugar. |
| Ubicacion (detalle) | `ubicacion_detalle` | `CharField` | Campo complementario al original «Ubicacion»; la fuente no fija longitud. |
| Activo Afectado | `activo_afectado` | `CharField(choices=...)` | Lista inicial de la Matriz Riesgos; validar que sea el catálogo autorizado. |
| Tipo Evento | `tipo_evento` | `CharField(choices=...)` | Lista inicial de la columna Riesgo de Matriz Riesgos; validar. |
| Descripcion | `descripcion` | `TextField` | Texto aportado por quien reporta. |
| Evidencias | `evidencias` | `FileField` | Acceso privado y validación de tamaño/contenido son requisitos; definir si admite varios archivos. |
| Estado general (F-GTI-08) | `estado_general` | `CharField(choices=...)` | Campo operativo adicional, no parte de los 13 campos F-GTI-01; flujo y opciones pendientes. |

El modelo institucional actual `Estado` representa departamentos geográficos en
la relación con `Ciudad`; no se debe reutilizar como estado del incidente.

Valores que aparecen en la Matriz Riesgos entregada:

- Activo Afectado: `Centro de Datos Principal`, `Servidores y estaciones`,
  `Correo institucional`, `Bases de datos`.
- Tipo Evento: `Caída General Internet`, `Ransomware`, `Phishing`,
  `Fuga de información`.

Son fuente para el borrador, no una aprobación para codificar opciones fijas.

### Clasificacion — F-GTI-02

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `incidente` | `OneToOneField(Incidente)` | Una clasificación por incidente es provisional; confirmar reclasificación/historial. |
| Fecha Registro | `fecha_registro` | `DateField` | La fuente permite que la registre la aplicación o quien registra. |
| Analista | `analista` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Modelo institucional por verificar. |
| Area Responsable | `area_responsable` | `ForeignKey(APP_INSTITUCIONAL.EstructuraOrganica)` | Distinta de la Dependencia reportante. |
| Ticket | `ticket` | `CharField(blank=True)` | Se recomienda opcional mientras se confirma la mesa de ayuda. |
| Clasificacion | `clasificacion` | `CharField(choices=...)` | La lista puede derivarse de Tipo Evento/Matriz Riesgos; confirmar semántica. |
| Criticidad | `criticidad` | `CharField(choices=...)` | Valores documentados en SLA: Bajo, Medio, Alto, Crítico. Confirmar valor almacenado y si se permite edición. |
| Usuarios Afectados | `usuarios_afectados` | `IntegerField` + mínimo 0 | El control de mínimo 0 procede del requisito RNF de conteos no negativos. |
| Disponibilidad | `disponibilidad` | `CharField(choices=...)` | La fuente no define las opciones. |
| Integridad | `integridad` | `CharField(choices=...)` | La fuente no define las opciones. |
| Confidencialidad | `confidencialidad` | `CharField(choices=...)` | La fuente no define las opciones. |
| Responsable | `responsable` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Persona responsable de atender; distinta del analista. |

### Investigacion — F-GTI-03

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `incidente` | `OneToOneField(Incidente)` | Cardinalidad provisional; confirmar varias investigaciones/historial. |
| Fecha Inicio | `fecha_inicio` | `DateField` | La registra el investigador o la aplicación. |
| Investigador | `investigador` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Modelo institucional por verificar. |
| Activo | `activo` | `CharField(choices=...)` | Lista derivada inicialmente de F-GTI-01; confirmar si existe catálogo de equipos. |
| Inventario | `inventario` | `CharField` | Código de inventario institucional si existe. |
| Criticidad | `incidente.clasificacion.criticidad` | Derivado, no columna | Mostrar la clasificación de F-GTI-02, evitando duplicación. Confirmar si se permite cambiar aquí. |
| Causa Inmediata | `causa_inmediata` | `TextField` | Texto de investigación. |
| Causa Raiz | `causa_raiz` | `TextField` | Texto de investigación. |
| Vulnerabilidad | `vulnerabilidad` | `TextField` | Texto de investigación. |
| Origen | `origen` | `CharField(choices=...)` | Opciones por confirmar. |
| Alcance | `alcance` | `TextField` | Texto de investigación. |
| Area Afectada | `area_afectada` | `ForeignKey(APP_INSTITUCIONAL.EstructuraOrganica)` | Campo adicional propuesto; no sustituye Dependencia ni Area Responsable. |
| Evidencias | `evidencias` | `FileField` | Privado y validado; confirmar si puede haber varios archivos. |

El formulario fuente identifica 12 campos originales más `Area Afectada`, para
13 en total.

### AccionIncidente — F-GTI-04

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `incidente` | `ForeignKey(Incidente)` | Varias acciones por incidente, explícito en el plan. |
| Actividad | `actividad` | `TextField` | Una fila por actividad para no sobrescribir acciones previas. |
| Tipo (Contencion/Erradicacion) | `tipo` | `CharField(choices=...)` | Opciones documentadas: Contención, Erradicación. |
| Responsable | `responsable` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Persona responsable de esa acción. |
| Fecha | `fecha` | `DateField` | Fecha de la acción. |
| Hora | `hora` | `TimeField` | Hora de la acción. |
| Estado | `estado` | `CharField(choices=...)` | Estado independiente por acción; opciones no definidas por la fuente. |
| Observaciones | `observaciones` | `TextField` | Texto libre. |

### Recuperacion — F-GTI-05

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `incidente` | `OneToOneField(Incidente)` provisional | Si hay más de un servicio afectado, podría requerirse `ForeignKey`. |
| Servicio | `servicio` | `CharField` | Nombre del servicio afectado. |
| Fecha Inicio | `fecha_inicio` | `DateField` | La fuente no define si incluye hora. |
| Fecha Fin | `fecha_fin` | `DateField(null=True, blank=True)` | Puede quedar pendiente mientras el servicio se recupera. |
| Responsable | `responsable` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Persona responsable de recuperación. |
| Servicio Operativo | `servicio_operativo` | `BooleanField(null=True)` | Confirmación sí/no; `null` representa no confirmado, no equivale a «No». |
| Aplicaciones Validadas | `aplicaciones_validadas` | `TextField` | La fuente acepta lista o texto largo. |
| Usuarios Verifican | `usuarios_verifican` | `BooleanField(null=True)` | Significado exacto por confirmar. |
| Observaciones | `observaciones` | `TextField` | Texto libre. |

### Cierre — F-GTI-06

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `incidente` | `OneToOneField(Incidente)` provisional | Confirmar reapertura y cierres sucesivos. |
| Fecha Cierre | `fecha_cierre` | `DateField` | La fuente permite fecha de aplicación o indicada por responsable. |
| Responsable | `responsable` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Aclarar si es quien cierra, quien autoriza o ambos. |
| Area | `area` | `ForeignKey(APP_INSTITUCIONAL.EstructuraOrganica)` | Área relacionada con el cierre. |
| Resumen | `resumen` | `TextField` | Resumen del cierre. |
| Usuarios Afectados | `incidente.clasificacion.usuarios_afectados` | Derivado, no columna | Fuente F-GTI-02. |
| Tiempo Indisponibilidad | `tiempo_indisponibilidad` | `DurationField(null=True, blank=True)` | No calcular si no existen datos de inicio y restablecimiento suficientes. |
| Sistemas Afectados | `sistemas_afectados` | `TextField` | La fuente permite consultar activos/sistemas previos. |
| Costo Total | `costo_total` | `DecimalField` | El Excel propone DecimalField(12,2); precisión/escala sujetas a aprobación. Si se desconoce, dejar pendiente; no sustituir por cero. |

### Leccion — F-GTI-07

| Campo original | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| No Incidente | `incidente` | `OneToOneField(Incidente)` provisional | Confirmar si se permite más de una revisión. |
| Fecha | `fecha` | `DateField` | Fecha de revisión de lo ocurrido. |
| Responsable | `responsable` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Quien revisa/registra la lección. |
| Que ocurrio | `que_ocurrio` | `TextField` | Texto de lección. |
| Por que ocurrio | `por_que_ocurrio` | `TextField` | Texto de lección; puede consultar la investigación. |
| Que funciono | `que_funciono` | `TextField` | Texto de lección. |
| Que mejorar | `que_mejorar` | `TextField` | Texto de lección. |
| Evitar recurrencia | `evitar_recurrencia` | `TextField` | Los Word actualizados indican texto largo. El Excel sugiere BooleanField: discrepancia pendiente de validación; se conserva texto en este borrador. |
| Accion | `AccionMejora.accion` | `TextField` en entidad hija | Una mejora por fila; permite conservar varias acciones independientes. |
| Responsable Accion | `AccionMejora.responsable_accion` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Quien ejecuta la mejora, distinto de quien registra la lección. |
| Fecha Inicio | `AccionMejora.fecha_inicio` | `DateField` | Fecha de la mejora. |
| Fecha Fin | `AccionMejora.fecha_fin` | `DateField(null=True, blank=True)` | Permitir pendiente mientras no termine requiere confirmación del equipo. |
| Estado | `AccionMejora.estado` | `CharField(choices=...)` | Estado propio de cada mejora; opciones por confirmar. |

### AccionMejora — desglose de F-GTI-07

| Campo | Atributo propuesto | Tipo Django | Notas |
|---|---|---|---|
| PK | `id` | `BigAutoField` | Propuesta técnica. |
| Lección | `leccion` | `ForeignKey(Leccion)` | Cada mejora pertenece a una lección y por ella al mismo incidente. |
| Accion | `accion` | `TextField` | Texto de la mejora propuesta. |
| Responsable Accion | `responsable_accion` | `ForeignKey(APP_INSTITUCIONAL.Persona)` | Responsable de ejecutarla. |
| Fecha Inicio | `fecha_inicio` | `DateField` | Inicio de la acción. |
| Fecha Fin | `fecha_fin` | `DateField(null=True, blank=True)` | Fin pendiente requiere aprobación. |
| Estado | `estado` | `CharField(choices=...)` | Independiente por acción; lista no definida. |

## Boceto de cardinalidades Django

Este extracto muestra únicamente la intención de las relaciones. Los objetivos
`APP_INSTITUCIONAL.*` y `on_delete` son marcadores/propuestas y deben sustituirse
después de verificar la aplicación institucional y sus reglas de retención.

```python
class Clasificacion(models.Model):
    incidente = models.OneToOneField("ciberseguridad.Incidente", ...)


class Investigacion(models.Model):
    incidente = models.OneToOneField("ciberseguridad.Incidente", ...)
    area_afectada = models.ForeignKey("APP_INSTITUCIONAL.EstructuraOrganica", ...)


class AccionIncidente(models.Model):
    incidente = models.ForeignKey("ciberseguridad.Incidente", ...)


class Recuperacion(models.Model):
    incidente = models.OneToOneField("ciberseguridad.Incidente", ...)  # provisional


class Cierre(models.Model):
    incidente = models.OneToOneField("ciberseguridad.Incidente", ...)  # provisional


class Leccion(models.Model):
    incidente = models.OneToOneField("ciberseguridad.Incidente", ...)  # provisional


class AccionMejora(models.Model):
    leccion = models.ForeignKey("ciberseguridad.Leccion", ...)
```

Los puntos suspensivos hacen que el extracto no sea ejecutable. No copiar a
`models.py` sin completar la validación y aprobación.


## Alcance de la evidencia verificada el 11/11/2026

Se contrastaron los campos con los Word actualizados de planificación y
formularios y con la hoja CAMPOS F-GTI del Excel de control disponible. El
Excel original UNISARC_Formularios_Ciberseguridad.xlsx y modelo_gral.docx se
mencionan como antecedentes; no estaban disponibles como archivos independientes
en la carpeta fuente examinada en esta revisión.

La matriz 04-trazabilidad-campos.csv conserva los 96 nombres de campo del
control (95 originales referidos por este y Área afectada adicional). Cubrir
96 filas de diseño no equivale a tener 96 campos implementados o aprobados.

El borrador usa las precisiones de los Word para Evitar recurrencia (texto),
Usuarios Verifican (sí/no) y Tiempo Indisponibilidad (duración). El Excel
contiene sugerencias diferentes en algunos tipos y recomienda un modelo de
evidencias vinculado; se debe acordar si se necesita una entidad hija con varios
archivos en vez de un FileField único. No se implementa ninguna opción todavía.

Todas las relaciones institucionales usarán las entidades existentes verificadas
al integrar SAIUNISARC. Los marcadores APP_INSTITUCIONAL no son nombres reales
confirmados ni código listo para ejecutar. Las reglas de borrado y obligatoriedad,
el historial y las decisiones de captura frente a datos derivados siguen abiertas.
