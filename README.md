```
Nombre del documento: README — Gobierno del Conocimiento
Código: LV-GOB-001
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: —
Aprobador: Dirección General
Estado: Vigente
```

# Gobierno del Conocimiento — La Ventanería Ingeniería y Diseño S.A.S.

## Propósito de esta carpeta

`00_GOBIERNO_CONOCIMIENTO` es la raíz de gobierno del repositorio `LA_VENTANERIA_CONOCIMIENTO`. Contiene las reglas que determinan cómo se crea, clasifica, versiona, aprueba, prioriza y audita el conocimiento de las 12 áreas de la empresa (Dirección, Comercial, Marketing, Redes Sociales, Ingeniería, Jurídico, Compras, Producción, Almacén, Contabilidad, Recursos Humanos y Servicio al Cliente).

Esta carpeta se numera `00_` a propósito: **las reglas del sistema van antes que el contenido de cualquier departamento**, incluida Dirección.

## Qué NO vive aquí

- Conocimiento operativo de un departamento específico (vive en su carpeta `0X_AREA`, una vez se ejecuten las fases correspondientes).
- Instrucciones de comportamiento de la IA (viven en `SKILL.md`, fuera de este repositorio — ver `01_ARQUITECTURA_MAESTRA.md`).
- Documentos originales firmados, expedientes o cifras reales (viven en Google Drive, fuera de GitHub — ver `01_ARQUITECTURA_MAESTRA.md`).

## Contenido de esta carpeta

| Archivo | Código | Contenido |
|---|---|---|
| `README.md` | LV-GOB-001 | Este documento |
| `01_ARQUITECTURA_MAESTRA.md` | LV-GOB-002 | Las 4 capas del sistema y la declaración de fuente maestra |
| `02_NIVELES_CONFIDENCIALIDAD.md` | LV-GOB-003 | Los 4 niveles de clasificación y quién accede a cada uno |
| `03_REGLAS_VERSIONAMIENTO.md` | LV-GOB-004 | Nomenclatura, estados, control de versiones, pipeline de incorporación |
| `04_REGLAS_PRIORIDAD_CONFLICTOS.md` | LV-GOB-005 | Qué hacer cuando dos fuentes difieren |
| `05_HISTORICO_DECISIONES_GOBIERNO.md` | LV-GOB-006 | Bitácora de decisiones sobre la arquitectura y registro de auditorías |
| `06_MATRIZ_MIGRACION_SKILL_A_GITHUB.md` | LV-GOB-007 | Registro de qué migra desde `references/` de la skill, hacia dónde, y en qué fase |

## Nomenclatura oficial de documentos

Todo documento del repositorio se identifica con el código:

```
LV-[ÁREA]-[###]
```

`LV` = La Ventanería. `[ÁREA]` = abreviatura del área (ver tabla completa en `03_REGLAS_VERSIONAMIENTO.md`). `[###]` = consecutivo de 3 dígitos. El código no incluye el tipo de documento — esa es una decisión deliberada, aprobada por Dirección, para mantener el esquema simple.

## Principio rector

**"UN DATO MAESTRO = UNA ÚNICA FUENTE OFICIAL."** Ningún documento de gobierno se duplica ni se resume en otra carpeta del repositorio. Cuando un departamento necesite citar una regla de gobierno, la referencia — no la copia.

## Orden de lectura recomendado

1. `01_ARQUITECTURA_MAESTRA.md`
2. `02_NIVELES_CONFIDENCIALIDAD.md`
3. `03_REGLAS_VERSIONAMIENTO.md`
4. `04_REGLAS_PRIORIDAD_CONFLICTOS.md`
5. `05_HISTORICO_DECISIONES_GOBIERNO.md`
6. `06_MATRIZ_MIGRACION_SKILL_A_GITHUB.md`

## Estado de ejecución de la arquitectura

Esta carpeta corresponde a la **Fase 0** de la hoja de ruta de construcción del repositorio. Las 12 carpetas de departamento (Fases 1 a 6) aún no han sido creadas. Ningún archivo de `references/` (skill del Director General) ha sido migrado todavía. `SKILL.md` no ha sido modificado ni migrado.
