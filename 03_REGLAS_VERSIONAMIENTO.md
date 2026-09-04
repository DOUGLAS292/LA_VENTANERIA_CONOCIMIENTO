```
Nombre del documento: Reglas de Versionamiento y Nomenclatura
Código: LV-GOB-004
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: —
Aprobador: Dirección General
Estado: Vigente
```

# Reglas de Versionamiento y Nomenclatura

## 1. Nomenclatura oficial de documentos

```
LV-[ÁREA]-[###]
```

`LV` = La Ventanería. `[###]` = consecutivo de 3 dígitos. El código **no incluye el tipo de documento** — decisión deliberada para mantener el esquema simple. Esto significa que el código por sí solo no indica si un documento es un proceso, una política o una plantilla; eso se identifica en el campo "Nombre del documento" del encabezado.

### Tabla de abreviaturas de área

| Área | Abreviatura | Ejemplo |
|---|---|---|
| Gobierno del Conocimiento | GOB | LV-GOB-001 |
| Dirección | DIR | LV-DIR-001 |
| Comercial | COM | LV-COM-001 |
| Marketing | MKT | LV-MKT-001 |
| Redes Sociales | RS | LV-RS-001 |
| Ingeniería | ING | LV-ING-001 |
| Jurídico | JUR | LV-JUR-001 |
| Compras | COMPR | LV-COMPR-001 |
| Producción | PROD | LV-PROD-001 |
| Almacén | ALM | LV-ALM-001 |
| Contabilidad | CONT | LV-CONT-001 |
| Recursos Humanos | RH | LV-RH-001 |
| Servicio al Cliente | SC | LV-SC-001 |

## 2. Metadato obligatorio en todo documento

Todo documento operativo de las 12 áreas y de gobierno lleva, sin excepción, este encabezado:

```
Nombre del documento:
Código:
Versión:
Fecha:
Responsable:
Revisor:
Aprobador:
Estado:
```

## 3. Estados y transición

| Estado | Significado | Quién puede moverlo a este estado |
|---|---|---|
| **Borrador** | En construcción, no usable como referencia oficial | El responsable del área |
| **En revisión** | Sometido a validación técnica/jurídica/financiera/laboral según corresponda | El revisor competente asignado |
| **Vigente** | Aprobado y válido como fuente oficial | Dirección, o el responsable de área en quien Dirección delegue formalmente (ver §6) |
| **Obsoleto** | Reemplazado por una versión posterior o ya no aplica | Dirección, al aprobar la nueva versión |

Un documento **nunca pasa directamente de Borrador a Vigente** cuando su naturaleza exige revisión profesional (ver §4) — debe pasar por En revisión.

## 4. Documentos que requieren revisión profesional obligatoria antes de Vigente

| Tipo de contenido | Revisor obligatorio |
|---|---|
| Cálculo estructural, especificación técnica, cumplimiento normativo (NSR-10 y afines) | Ingeniero estructural responsable |
| Contratos, casos legales, clasificación contractual laboral | Abogado responsable |
| Cifras financieras, tributarias, esquemas de pago | Contador / revisor fiscal |
| Normativa laboral, de protección al consumidor o cualquier norma citada como fundamento de una decisión | Verificación de vigencia por el profesional competente antes de fijarla como Vigente — nunca de memoria |

## 5. Control de versiones — regla fundamental

**Nunca sobrescribir una versión Vigente.** Una modificación sustancial genera una nueva versión (v1.1, v2.0, etc.).

**El historial de control de versiones se conserva mediante el historial de Git — no se crean archivos separados con sufijo `_OBSOLETO`.** Git ya conserva cada versión anterior de forma nativa; duplicar archivos obsoletos ensuciaría la estructura y violaría el principio de una única fuente oficial.

"Obsoleto" no significa "borrado". Significa que ya no debe utilizarse como instrucción vigente, pero permanece disponible en el historial de Git para trazabilidad.

### Retención

- **Documentos normales:** se conservan todas las versiones aprobadas mientras tengan valor histórico, vía historial de Git.
- **Documentos jurídicos, contables, laborales, contractuales y financieros:** no se establece aquí un plazo de eliminación. Su conservación se rige por las obligaciones legales, tributarias, contractuales y de archivo que correspondan **(PENDIENTE DE APROBACIÓN la verificación puntual de esos plazos con el profesional competente cuando se documente cada caso concreto)**.
- **Borradores nunca aprobados:** pueden eliminarse cuando dejen de tener utilidad, dejando constancia cuando sea necesario.

## 6. Delegación de aprobación

Dirección conserva la autoridad final sobre gobierno, estrategia y decisiones de alto impacto, y **puede delegar formalmente** la aprobación de documentos operativos a responsables de área.

**Dirección debe aprobar obligatoriamente:**
- Políticas corporativas.
- Cambios estratégicos.
- Cambios de estructura organizacional.
- Políticas comerciales críticas.
- Cambios que afecten varias áreas.
- Decisiones que impliquen riesgo financiero, jurídico o reputacional significativo.
- Cambios en las reglas de Gobierno del Conocimiento.
- Excepciones a las reglas maestras.

**Condición operativa actual:** mientras no exista una matriz formal de responsables por área, **Dirección (Douglas Castillo) es el aprobador por defecto de todos los documentos de todas las áreas.** No se fabrican responsables de área que todavía no han sido formalmente designados.

**Separación de funciones:** crear un documento no equivale a aprobarlo. Quien redacta puede ser distinto de quien revisa, y distinto de quien aprueba. Esto aplica incluso cuando, en la práctica actual, Dirección ocupe más de uno de esos roles por ausencia de responsables designados.

## 7. Reglas para referencias a documentos externos (Capa 3, Google Drive)

Cuando un documento de GitHub necesite citar un documento original en Drive:

1. Nunca se copia el contenido completo — se describe su estructura o contenido relevante.
2. Se indica: nombre del documento, ubicación conocida en Drive (o referencia al índice restringido si aplica), fecha del documento original, y si es necesario solicitar acceso.
3. Si el documento original cambia, quien lo detecte debe señalar la desactualización de la referencia en GitHub — no se asume sincronía automática.

## 8. Pipeline permanente de incorporación de conocimiento

| Etapa | Qué ocurre | Responsable |
|---|---|---|
| **1. Clasificación** | Se determina tipo de contenido y nivel de confidencialidad | Responsable del área de origen (o Dirección, mientras no exista responsable formal) |
| **2. Revisión** | Si aplica (§4), pasa por el profesional competente | Revisor asignado |
| **3. Aprobación** | Se confirma que puede fijarse como Vigente | Dirección, o responsable de área delegado |
| **4. GitHub** | Se sube con metadato completo (§2) y estado correspondiente | Responsable del área, tras aprobación |

Este pipeline es **permanente**: aplica a toda incorporación futura de conocimiento, no solo a la migración inicial de `references/`.

## 9. Auditoría y trazabilidad

- **Auditoría documental:** trimestral. Revisión de documentos vigentes, obsoletos, versiones, responsables, documentos pendientes de aprobación, enlaces/referencias, contradicciones y estructura del repositorio.
- **Auditoría de accesos:** semestral. Revisión de quién tiene acceso al repositorio, quién tiene acceso a CONFIDENCIAL/RESTRINGIDO, personas que ya no trabajan con la empresa, permisos innecesarios y cuentas externas.
- **Auditoría extraordinaria:** inmediata ante cambio importante de estructura empresarial, incidente de seguridad, cambio legal relevante, modificación importante de un proceso, cambio de responsable de área, sospecha de información incorrecta, o incorporación de una nueva fuente de conocimiento crítica.
- **Responsable de convocar las tres auditorías:** Dirección, por defecto, mientras no exista delegación formal.
- **Registro de cada auditoría:** se documenta en `05_HISTORICO_DECISIONES_GOBIERNO.md` — no se crea un documento aparte.
- **Corrección inmediata:** no se espera a la auditoría periódica para corregir un error crítico. Si alguien detecta que un documento Vigente contiene información incorrecta, debe marcarse de inmediato como **"En revisión"** y escalarse al responsable correspondiente.
