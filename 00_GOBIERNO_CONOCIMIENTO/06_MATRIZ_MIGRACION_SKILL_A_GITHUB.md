```
Nombre del documento: Matriz de Migración — Skill/references/ a GitHub
Código: LV-GOB-007
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: Ver columna "Revisión profesional"
Aprobador: Dirección General (por ejecutar en cada fase)
Estado: Vigente como plan — ninguna fila ejecutada todavía
```

# Matriz de Migración — `references/` (skill) → GitHub

## Propósito

Registro oficial de qué conocimiento migra desde `SKILL.md` + `references/` hacia el repositorio `LA_VENTANERIA_CONOCIMIENTO`, hacia qué ruta exacta, con qué controles, y en qué fase de la hoja de ruta aprobada. Esta tabla es el plan — ninguna fila se ha ejecutado. Cada migración real seguirá el pipeline permanente definido en `03_REGLAS_VERSIONAMIENTO.md` §8: **CLASIFICACIÓN → REVISIÓN → APROBACIÓN → GITHUB.**

## Matriz

| Archivo actual | Departamento | Tipo de información | Destino GitHub (código propuesto) | Confidencialidad | Aprobación | Revisión profesional | Fase | Estado |
|---|---|---|---|---|---|---|---|---|
| `SKILL.md` | Transversal | Instrucciones de IA | No se migra — permanece en Capa 2 | INTERNO | No aplica | No aplica | — | No aplica |
| `comercial.md` | Comercial | Índice operativo | `02_COMERCIAL/README.md` (fusión) — `LV-COM-001` | INTERNO | Sí | No | **Fase 4** | Pendiente |
| `ingenieria.md` | Ingeniería | Caso real (Tuluá, hallazgo de no conformidad) | `05_INGENIERIA/07_CASOS_Y_LECCIONES_APRENDIDAS/` — `LV-ING-001` | CONFIDENCIAL | Sí | **Sí — ingeniero estructural** | **Fase 5** | Pendiente |
| `juridico.md` | Jurídico | Casos activos (incluye caso de fraude bancario) | `06_JURIDICO/08_INDICE_DOCUMENTOS_RESTRINGIDOS/` — `LV-JUR-001` | **RESTRINGIDO** | Sí | **Sí — abogado responsable** | **Fase 6** | Pendiente |
| `compras.md` | Compras | Parámetros técnicos de optimización, estructura de `OF_COMPLETA.xlsx` | `07_COMPRAS/04_REFERENCIA_TECNICA_NORMATIVA/` — `LV-COMPR-001` | CONFIDENCIAL | Sí | Recomendable | **Fase 5** | Pendiente |
| `produccion.md` | Producción | Caso real (orden de 18 ventanas multisistema) | `08_PRODUCCION/05_DECISIONES_E_HISTORICO/` — `LV-PROD-001` | INTERNO/CONFIDENCIAL* | Sí | Recomendable | **Fase 5** | Pendiente |
| `almacen.md` | Almacén | Sin contenido real — solo pendientes | `09_ALMACEN/01_PROCESOS/` (consolidar como punto de partida) — `LV-ALM-001` | N/A | N/A | N/A | **Fase 3** | Pendiente |
| `contabilidad.md` | Contabilidad | Esquema de pago a colaboradores | `10_CONTABILIDAD/02_POLITICAS_Y_REGLAS/` — `LV-CONT-001` | CONFIDENCIAL | Sí | Recomendable | **Fase 6** | Pendiente |
| `marketing.md` | Marketing | Estrategia de contenido, iniciativas VentanaAR y podcast | `03_MARKETING/01_PROCESOS/` + `05_DECISIONES_E_HISTORICO/` — `LV-MKT-001` | INTERNO | Sí | No | **Fase 4** | Pendiente |
| `rrhh.md` | Recursos Humanos | Modalidad de contratación, nomenclatura contractual | `11_RECURSOS_HUMANOS/02_POLITICAS_Y_REGLAS/` — `LV-RH-001` | CONFIDENCIAL | Sí | **Sí — abogado laboralista** | **Fase 6** | Pendiente |
| `servicio_cliente.md` | Servicio al Cliente | Referencia normativa (Ley 1480/2011) | `12_SERVICIO_CLIENTE/04_REFERENCIA_TECNICA_NORMATIVA/` — `LV-SC-001` | INTERNO | Sí | **Sí — verificar vigencia de la norma** | **Fase 5 (cierre)** | Pendiente |

*Sube a CONFIDENCIAL si el caso identifica un cliente específico — a confirmar al ejecutar la migración.

## Reglas aplicables a toda fila de esta matriz

1. Ninguna fila se ejecuta fuera de la fase asignada, salvo decisión explícita de Dirección que reordene la hoja de ruta.
2. Toda fila marcada con revisión profesional obligatoria no puede quedar en estado "Vigente" sin que esa revisión se haya completado y quede registrada.
3. Al ejecutar cada fila, este documento se actualiza cambiando su columna "Estado" de "Pendiente" a "Ejecutada", y se agrega la fecha de ejecución — no se elimina ni se reescribe la fila.
4. La ejecución de cada fila debe generar, además, una entrada correspondiente en `05_HISTORICO_DECISIONES_GOBIERNO.md`.
