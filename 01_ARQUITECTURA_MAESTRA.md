```
Nombre del documento: Arquitectura Maestra del Conocimiento
Código: LV-GOB-002
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: —
Aprobador: Dirección General
Estado: Vigente
```

# Arquitectura Maestra del Conocimiento

## 1. Declaración de fuente maestra

**El repositorio GitHub `LA_VENTANERIA_CONOCIMIENTO` es la FUENTE MAESTRA del conocimiento empresarial de La Ventanería Ingeniería y Diseño S.A.S.** Ningún otro sistema —skill de IA, chats, correo, Google Drive, cuentas dispersas— tiene autoridad para contradecirlo una vez que un documento alcanza el estado **Vigente** (ver `03_REGLAS_VERSIONAMIENTO.md`).

Esta condición existe porque GitHub es el único sistema disponible con control de versiones real, historial auditable, e independencia de cuál asistente de IA se use.

## 2. Las cuatro capas del sistema de conocimiento

| Capa | Qué contiene | Dónde vive | Quién la gobierna |
|---|---|---|---|
| **Capa 0 — Gobierno** | Las reglas de este mismo sistema | `00_GOBIERNO_CONOCIMIENTO/` | Dirección General |
| **Capa 1 — Documentación operativa** | Procesos, políticas, plantillas, referencia técnica/normativa, decisiones, indicadores, casos, e índices restringidos de las 12 áreas | `01_DIRECCION/` … `12_SERVICIO_CLIENTE/` en GitHub | Responsable de cada área (cuando exista) + Dirección para lo Vigente |
| **Capa 2 — Instrucciones de comportamiento de IA** | Persona del asistente, principios rectores de cómo debe responder, reglas de cuándo consultar cada carpeta | `SKILL.md` y el prompt del proyecto — **fuera de este repositorio** | Dirección |
| **Capa 3 — Documentos originales** | Contratos firmados, estados financieros, expedientes legales, memorias de cálculo selladas, archivos Excel con datos vivos, archivos CAD/BIM | **Google Drive** — fuera de GitHub | El área dueña del documento |

**Regla dura:** ningún dato cruza de capa sin pasar por su regla propia. La Capa 1 no contiene datos personales/financieros/legales completos (esos son Capa 3, solo referenciados). La Capa 2 no contiene hechos de la empresa (esos son Capa 1). La Capa 0 no contiene ni lo uno ni lo otro — solo reglas.

## 3. Separación entre conocimiento empresarial e instrucciones de IA

Esta separación es el principio que originó esta arquitectura. Regla operativa:

- Si la pregunta es **"¿qué es cierto sobre la empresa?"** → Capa 1 (GitHub).
- Si la pregunta es **"¿cómo debe comportarse la IA al usar ese dato?"** → Capa 2 (`SKILL.md`).

`SKILL.md` **no debe migrarse como conocimiento empresarial** bajo ninguna circunstancia. Permanece como capa de comportamiento, separada de los datos de la empresa.

## 4. Google Drive como ubicación de documentos originales

**Google Drive es la ubicación de los documentos originales de la empresa.** GitHub no almacena originales sensibles: Excel originales, PDF firmados, contratos, memorias de cálculo, fichas técnicas originales, documentos contables, expedientes jurídicos, ni documentos con datos personales.

GitHub conserva el documento de conocimiento estructurado y, cuando corresponda, una referencia al original. Ejemplo de estructura:

```
05_INGENIERIA/
└── 04_REFERENCIA_TECNICA_NORMATIVA/
    └── LV-ING-003.md
```

Dentro de `LV-ING-003.md`:

```
DOCUMENTO ORIGINAL: OF_COMPLETA.xlsx
UBICACIÓN: Google Drive / Ingeniería / Producción
TIPO: Archivo fuente original
ESTADO: Vigente
RESPONSABLE: Ingeniería
```

**PENDIENTE DE IMPLEMENTACIÓN:** la cuenta/Drive corporativo oficial (de entre las múltiples cuentas de Google identificadas: personal de Dirección, cuenta genérica de la empresa, cuenta operativa, y cuentas de terceros) todavía no ha sido designada formalmente. Mientras esto no se resuelva, cualquier referencia a una ubicación de Drive se documenta como "ubicación conocida", no como "ubicación oficial".

## 5. Índice de documentos restringidos

Cada área que lo requiera tendrá una subcarpeta **`08_INDICE_DOCUMENTOS_RESTRINGIDOS`**. Esta carpeta **nunca contiene el documento sensible original** — únicamente:

| Campo del índice | Descripción |
|---|---|
| Nombre del documento | Título identificador, sin datos sensibles en el nombre del archivo |
| Clasificación | PÚBLICO / INTERNO / CONFIDENCIAL / RESTRINGIDO (ver `02_NIVELES_CONFIDENCIALIDAD.md`) |
| Ubicación real | Dónde vive el documento original (Capa 3, Google Drive) |
| Responsable | Quién lo custodia |
| Control de acceso | Quién puede solicitarlo y cómo |
| Fecha de último control | Cuándo se verificó que sigue existiendo y vigente |

## 6. Regla de referencia a documentos externos

Ningún documento original se transcribe completo dentro de un `.md` de GitHub. La Capa 1 solo puede:
1. Describir su estructura o contenido de forma resumida.
2. Apuntar a su ubicación mediante el índice (si es sensible) o una referencia directa (si no lo es).

## 7. Registros y evidencias (concepto opcional)

Se incorpora la categoría **REGISTROS/EVIDENCIAS**, distinta de `05_DECISIONES_E_HISTORICO`:

- **Decisiones e histórico** = registro narrativo de una decisión tomada (qué se decidió, por qué, quién aprobó).
- **Registros/Evidencias** = hechos brutos con valor probatorio, sin narrativa de decisión (ej.: fotografías de una no conformidad en Producción, un ensayo de laboratorio en Ingeniería, un formato de visita técnica firmado en Servicio al Cliente).

No todas las áreas necesitan esta subcarpeta. Se activa **solo cuando el área genere evidencia física o documental repetible** que deba conservarse con trazabilidad — se decide caso por caso al construir cada área.

## 8. Pipeline permanente de incorporación de conocimiento

Todo conocimiento nuevo —no solo la migración inicial de `references/`— entra a GitHub exclusivamente por:

**CLASIFICACIÓN → REVISIÓN → APROBACIÓN → GITHUB**

El detalle operativo de cada etapa está en `03_REGLAS_VERSIONAMIENTO.md`. Este pipeline es **permanente y no excepcional**: no existe atajo para "solo esta vez".

## 9. Relación con la skill del Director General

La skill sigue operando como interfaz conversacional (Capa 2), pero deja de ser depósito de datos empresariales. Su tabla de enrutamiento por departamento debe, a partir de la migración (Fase 2 en adelante), apuntar a las rutas de GitHub en vez de contener el conocimiento ella misma.

## 10. Clasificación documental vs. control técnico de acceso

**La clasificación documental (PÚBLICO / INTERNO / CONFIDENCIAL / RESTRINGIDO) no sustituye los controles técnicos de acceso.** La información CONFIDENCIAL y RESTRINGIDA debe almacenarse en ubicaciones cuyo control de acceso técnico sea compatible con su nivel de clasificación.

```
GitHub
  │
  ├── conocimiento empresarial (Capa 1)
  │
  └── índice/referencia
            │
            ▼
      Google Drive
            │
            └── documento restringido (Capa 3)
```

**PENDIENTE DE IMPLEMENTACIÓN:** la configuración técnica real de acceso (visibilidad del repositorio, permisos por persona, y cómo mantener la conexión con Claude sin exponer el repositorio públicamente) no ha sido definida ni ejecutada. El repositorio **continúa temporalmente con su configuración actual**; este documento no autoriza ni ejecuta ningún cambio de visibilidad o permisos. Ver `02_NIVELES_CONFIDENCIALIDAD.md` §4 y el registro correspondiente en `05_HISTORICO_DECISIONES_GOBIERNO.md`.
