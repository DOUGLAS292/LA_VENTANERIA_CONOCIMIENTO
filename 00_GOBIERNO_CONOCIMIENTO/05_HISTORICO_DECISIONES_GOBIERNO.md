```
Nombre del documento: Histórico de Decisiones de Gobierno
Código: LV-GOB-006
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: —
Aprobador: Dirección General
Estado: Vigente
```

# Histórico de Decisiones de Gobierno

## Propósito

Bitácora permanente de decisiones sobre la arquitectura de gobierno del conocimiento y registro de auditorías ejecutadas. No documenta decisiones operativas de un departamento específico — esas viven en el `05_DECISIONES_E_HISTORICO` de cada área, cuando se construya.

Este documento **nunca se sobrescribe**: cada decisión o auditoría nueva se agrega como fila nueva, con fecha. Las filas anteriores no se editan ni se eliminan (ver `03_REGLAS_VERSIONAMIENTO.md` §5).

## Registro de decisiones de arquitectura

| Fecha | Decisión | Contexto | Aprobado por | Estado |
|---|---|---|---|---|
| 2026-08-26 | Se adopta arquitectura de 4 capas: Gobierno, Documentación operativa, Instrucciones de IA, Documentos originales | Diagnóstico reveló conocimiento empresarial real mezclado dentro de la skill de IA (`references/`) | Dirección | Adoptada |
| 2026-08-26 | GitHub `LA_VENTANERIA_CONOCIMIENTO` se declara FUENTE MAESTRA del conocimiento empresarial | Es el único sistema disponible con control de versiones real e independiente del asistente de IA usado | Dirección | Adoptada |
| 2026-08-26 | Se aprueba estructura interna de las 12 áreas con categorías evaluadas caso por caso, no uniformes | Evitar forzar subcarpetas sin contenido real que las justifique | Dirección | Adoptada |
| 2026-08-26 | La subcarpeta de documentos sensibles se denomina `08_INDICE_DOCUMENTOS_RESTRINGIDOS` (no `08_DOCUMENTOS_RESTRINGIDOS`) | Aclarar que esta carpeta nunca aloja el documento sensible original, solo su índice | Dirección | Adoptada |
| 2026-08-26 | Se incorpora la categoría REGISTROS/EVIDENCIAS como opcional, no obligatoria para todas las áreas | Distinguir evidencia bruta (fotos, ensayos, formatos firmados) de decisiones narrativas | Dirección | Adoptada |
| 2026-08-26 | Se establece el principio "UN DATO MAESTRO = UNA ÚNICA FUENTE OFICIAL" | Evitar que las 12 áreas o la skill generen versiones paralelas del mismo dato | Dirección | Adoptada |
| 2026-08-26 | El pipeline CLASIFICACIÓN → REVISIÓN → APROBACIÓN → GITHUB se declara permanente para toda incorporación futura de conocimiento, no solo para la migración inicial | Evitar que se repita el problema original de datos operativos viviendo fuera de la fuente maestra | Dirección | Adoptada |
| 2026-08-26 | Se aprueba hoja de ruta de 7 fases (0 a 6): Fase 0 Gobierno; Fase 1 Arquitectura de las 12 carpetas; Fase 2 Migración controlada de `references/`; Fase 3 Almacén (primer conocimiento operativo desde cero); Fase 4 Dirección + Comercial + Marketing + Redes Sociales; Fase 5 Ingeniería → Compras → Producción, cerrando con Servicio al Cliente; Fase 6 Jurídico + Contabilidad + Recursos Humanos | Secuenciar la construcción de menor a mayor riesgo/sensibilidad, aprovechando primero el conocimiento real ya existente en `references/` | Dirección | Adoptada |
| 2026-08-26 | Punto 1 de gobierno — Nomenclatura oficial de documentos: `LV-[ÁREA]-[###]`, sin tipo de documento en el código | Mantener el esquema de codificación simple | Dirección | Adoptada |
| 2026-08-26 | Punto 2 de gobierno — Google Drive es la ubicación de documentos originales; GitHub conserva el conocimiento estructurado y la referencia al original | Separar Capa 1 (documentación) de Capa 3 (originales) de forma operativa | Dirección | Adoptada — cuenta/Drive corporativo oficial queda PENDIENTE DE IMPLEMENTACIÓN |
| 2026-08-26 | Punto 3 de gobierno — Cuatro niveles de confidencialidad (PÚBLICO / INTERNO / CONFIDENCIAL / RESTRINGIDO) con acceso progresivo y autorización explícita para los dos niveles superiores; la IA debe respetar la clasificación y declarar cuando no tiene autorización o el documento no está disponible | Definir el "corazón de la seguridad" del sistema de conocimiento | Dirección | Adoptada — matriz nominal de accesos y control técnico real quedan PENDIENTE DE IMPLEMENTACIÓN |
| 2026-08-26 | Punto 4 de gobierno — Auditoría documental trimestral, auditoría de accesos semestral, auditoría extraordinaria ante evento relevante; corrección inmediata de errores críticos sin esperar auditoría periódica | Evitar que la clasificación y el estado de los documentos se degraden sin control | Dirección | Adoptada — Dirección responsable por defecto hasta que exista delegación formal |
| 2026-08-26 | Punto 5 de gobierno — Las versiones aprobadas se conservan mediante el historial de Git; no se crean archivos con sufijo `_OBSOLETO`; retención de documentos jurídicos/contables/laborales/contractuales sujeta a obligaciones legales aplicables | Evitar duplicación de archivos y aprovechar el control de versiones nativo de Git | Dirección | Adoptada |
| 2026-08-26 | Punto 6 de gobierno — Dirección conserva autoridad final sobre gobierno, estrategia y decisiones de alto impacto; puede delegar aprobación operativa por área cuando exista responsable formal; documentos técnicos/jurídicos/contables/laborales de alto riesgo requieren revisión profesional antes de Vigente; separación entre quien redacta, revisa y aprueba | Formalizar el circuito de aprobación sin inventar responsables inexistentes | Dirección | Adoptada — mientras no exista matriz formal de responsables por área, Dirección (Douglas Castillo) es el aprobador por defecto de todas las áreas |
| 2026-08-26 | Punto 7 de gobierno — La clasificación documental no sustituye el control técnico de acceso; el repositorio pasará a privado en una fase de configuración técnica futura, no ahora; los documentos altamente sensibles permanecen en Drive con referencia autorizada desde GitHub; la matriz real de usuarios/permisos se construirá cuando se defina la configuración técnica de GitHub + Claude + Drive | Separar explícitamente gobierno documental (quién debería poder ver algo) de control técnico (quién realmente puede verlo) | Dirección | Adoptada — configuración técnica de visibilidad y permisos queda expresamente PENDIENTE DE IMPLEMENTACIÓN; el repositorio continúa sin cambios de visibilidad ni permisos |
| 2026-08-26 | Fase 0 ejecutada: se crean los 7 documentos de `00_GOBIERNO_CONOCIMIENTO/` incorporando los 7 puntos de gobierno aprobados | Cierre formal de la Fase 0 de la hoja de ruta | Dirección | Ejecutada — entregada como archivos para incorporación manual al repositorio (ver nota de alcance en `README.md` del proyecto) |

## Registro de auditorías ejecutadas

*(Sin registros todavía — este documento se actualizará con cada auditoría documental trimestral, de accesos semestral, o extraordinaria que se ejecute, siguiendo el formato: Fecha | Tipo de auditoría | Hallazgos | Acciones tomadas | Responsable.)*

| Fecha | Tipo de auditoría | Hallazgos | Acciones tomadas | Responsable |
|---|---|---|---|---|
| — | — | — | — | — |

## Puntos abiertos que deberán resolverse y registrarse aquí cuando se decidan

- Cuenta/Drive corporativo oficial para documentos originales.
- Listado nominal de personas con acceso CONFIDENCIAL y RESTRINGIDO.
- Configuración técnica definitiva del repositorio (visibilidad, permisos, mantenimiento de la conexión con Claude).
- Delegación formal de aprobación a responsables de área, en la medida en que se designen.
- Periodicidad de revisión de los propios niveles de confidencialidad.
