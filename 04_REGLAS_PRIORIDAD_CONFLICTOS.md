```
Nombre del documento: Reglas de Prioridad y Resolución de Conflictos
Código: LV-GOB-005
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: —
Aprobador: Dirección General
Estado: Vigente
```

# Reglas de Prioridad y Resolución de Conflictos

## 1. Principio rector

**"UN DATO MAESTRO = UNA ÚNICA FUENTE OFICIAL."** Cuando exista más de una fuente sobre un mismo hecho, no se promedian, no se combinan y no se elige la más conveniente — se aplica la jerarquía siguiente.

## 2. Jerarquía general de fuentes

1. **Documento original firmado/aprobado** (Capa 3, Google Drive: contrato, factura, memoria de cálculo sellada) — siempre prevalece sobre cualquier resumen o transcripción.
2. **GitHub en estado Vigente**, con la fecha más reciente.
3. **Contenido aún en `references/` de la skill, no migrado** — se trata como **no oficial / pendiente de migrar**, nunca como verdad permanente, aunque hoy sea la única fuente disponible.
4. **Cualquier otra fuente dispersa** (Drive sin clasificar, correos, chats) — no tiene valor de fuente oficial hasta pasar por el pipeline de `03_REGLAS_VERSIONAMIENTO.md` §8.

Las demás áreas y sistemas **referencian** la fuente oficial; no generan una versión paralela del mismo dato.

## 3. Jerarquía específica para materias jurídicas y normativas

1. Fuentes oficiales del Estado colombiano.
2. Legislación y jurisprudencia oficial.
3. Documentos contractuales originales.
4. Conceptos de profesionales jurídicos competentes.
5. Fuentes secundarias, únicamente como apoyo.

**Regla dura:** ninguna norma se cita como vigente sin verificación en fuente oficial cuando sea determinante para una decisión — nunca de memoria.

## 4. Procedimiento cuando dos documentos difieren

| Paso | Acción |
|---|---|
| 1 | Identificar cuál de los dos documentos está en un estado más alto según §2 |
| 2 | Si ambos están en el mismo nivel, prevalece la fecha más reciente marcada como Vigente |
| 3 | Si la diferencia involucra materia técnica, jurídica, financiera o laboral de alto riesgo, se activa revisión profesional obligatoria (`03_REGLAS_VERSIONAMIENTO.md` §4) antes de resolver |
| 4 | Si no se puede resolver con los pasos anteriores, se escala a Dirección |
| 5 | La resolución final se registra en `05_HISTORICO_DECISIONES_GOBIERNO.md`, con fecha, responsable y justificación |

## 5. Regla especial: información aún no validada

Si un dato operativo (ej. una convención contractual, un parámetro técnico) se está usando activamente en la operación pero todavía no tiene revisión profesional formal, debe migrar a GitHub marcado explícitamente como **"En revisión"**, nunca como "Vigente", y debe conservar la advertencia de riesgo que ya tuviera en su fuente original.

Ejemplo ya identificado: la nomenclatura "Acuerdo de Prestación de Servicios" (Jurídico/RR.HH.) se usa activamente, pero su validez legal frente a la normativa laboral colombiana no ha sido confirmada. Al migrar, la advertencia de riesgo debe migrar con ella — no se puede fijar como regla cerrada sin esa salvedad.

## 6. Responsabilidad final

Ante cualquier conflicto no resuelto por las reglas anteriores, la decisión final es de Dirección General. Ninguna IA ni ningún colaborador puede fijar un documento como "Vigente" para resolver una contradicción por su cuenta.

## 7. Papel de la IA ante un conflicto detectado

Si Claude (u otro asistente operando sobre este repositorio) detecta una contradicción entre dos fuentes al responder una pregunta, debe:

1. Señalar explícitamente que existe una discrepancia, en vez de elegir silenciosamente una de las dos versiones.
2. Aplicar la jerarquía de §2 y §3 para indicar cuál fuente prevalece según la regla, dejando claro que es una aplicación de la regla y no una opinión propia.
3. Si la discrepancia es de alto riesgo (jurídico, financiero, técnico, laboral), señalar que requiere validación profesional antes de actuar sobre esa información.
