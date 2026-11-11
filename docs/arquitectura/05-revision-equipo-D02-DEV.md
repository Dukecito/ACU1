# Revisión del equipo — D02-DEV

Fecha de preparación: 11/11/2026. Responsable: Diego Alejandro Carvajal Garzón.
Estado: entregables preparados; revisión y aprobación pendientes.
Tiempo planificado: 4 h. Tiempo real: pendiente de registro por Diego.

| Decisión | Propuesta de diseño | Decisión del equipo / responsable |
|---|---|---|
| Entidades institucionales | Reutilizar Persona, Cargo, Sede y EstructuraOrganica; verificar app y tablas en SAIUNISARC | Pendiente |
| Identidad | Verificar enlace entre usuario autenticado y Persona; Persona.user local es texto | Pendiente |
| Etapas únicas | Clasificación, investigación, recuperación, cierre y lección 1:0..1 provisionales | Pendiente; confirmar historial y varios servicios |
| Acciones F04 | Incidente 1:0..N AccionIncidente | Pendiente de revisión |
| Mejoras F07 | Leccion 1:0..N AccionMejora | Pendiente de revisión |
| Áreas | Área afectada F03 → EstructuraOrganica; separar reportante/responsable/afectada | Pendiente |
| Evidencias | Definir FileField único o entidad hija de varios archivos; almacenamiento privado | Pendiente |
| Datos derivados | Criticidad F03 y usuarios afectados F06 desde F02; decidir si requieren instantáneas históricas | Pendiente |
| Reglas de integridad | Borrado, obligatoriedad, catálogos, código único, autorización de cierre | Pendiente |
| Conflictos fuente | Evitar recurrencia: texto Word / sí-no Excel; duración y precisión monetaria | Pendiente |
| RF-01 | El plan lo asigna a D02-DEV, pero la tarjeta D02 exige diseño. Autenticación institucional no está implementada ni verificada | Katerin y Chirley deben aclarar la asignación |

## Lista de comprobación

- [x] Proponer entidades, PK, FK y cardinalidades.
- [x] Preparar diagrama lógico y modelos borrador fuera de models.py.
- [x] Verificar correspondencia de 96 campos del control.
- [x] Comprobar la configuración actual de Django, sin migrar.
- [x] Preparar paquete local de evidencia para adjuntar.
- [ ] Revisar relaciones 1:1 y 1:N con el equipo.
- [ ] Manuela verifica la entrega y registra observaciones.
- [ ] Registrar horas reales de trabajo.
- [ ] Adjuntar evidencia y actualizar el control autorizado.

No se ha publicado evidencia ni cambiado el estado de Trello desde esta revisión.
No se debe marcar Hecho mientras falte la revisión exigida por la tarjeta.
