```
Nombre del documento: Niveles de Confidencialidad
Código: LV-GOB-003
Versión: 1.0
Fecha: 2026-08-26
Responsable: Dirección General (Douglas Castillo)
Revisor: PENDIENTE DE APROBACIÓN (asesor jurídico, para el tratamiento de datos personales)
Aprobador: Dirección General
Estado: Vigente
```

# Niveles de Confidencialidad

## 1. Los cuatro niveles

| Nivel | Acceso |
|---|---|
| **PÚBLICO** | Información que puede divulgarse externamente |
| **INTERNO** | Personal autorizado de La Ventanería |
| **CONFIDENCIAL** | Dirección + responsables específicamente autorizados |
| **RESTRINGIDO** | Solo responsables expresamente autorizados + Dirección cuando corresponda |

## 2. CONFIDENCIAL — ejemplos y acceso

Ejemplos: estrategia comercial; precios y márgenes; proveedores estratégicos; información financiera interna; contratos y negociaciones; información comercial de clientes; información técnica propietaria.

Acceso: Dirección + responsable del área + personas expresamente autorizadas.

## 3. RESTRINGIDO — ejemplos y acceso

Ejemplos: expedientes jurídicos activos; datos personales sensibles; información bancaria; información laboral confidencial; credenciales; información cuya divulgación pueda generar riesgo legal, financiero o de seguridad.

Acceso: únicamente las personas expresamente autorizadas para ese documento.

## 4. Regla de oro

**Estar dentro de la empresa NO significa tener acceso automático a todo.**

**La clasificación documental no sustituye los controles técnicos de acceso.** La información CONFIDENCIAL y RESTRINGIDA debe almacenarse en ubicaciones cuyo control de acceso técnico sea compatible con su nivel de clasificación. Un documento bien clasificado en un repositorio con acceso de lectura abierto no está protegido — solo está correctamente etiquetado.

**PENDIENTE DE IMPLEMENTACIÓN:** el mecanismo técnico que haga cumplir esta regla (permisos reales de lectura sobre el repositorio y sobre Google Drive) todavía no existe. Hasta que se implemente, la protección real de un documento CONFIDENCIAL o RESTRINGIDO depende exclusivamente de quién tiene acceso técnico de lectura al repositorio y a la carpeta de Drive correspondiente — no de esta clasificación por sí sola.

## 5. Papel de la IA frente a la clasificación

**La IA (Claude) no debe convertirse en una puerta para saltarse los permisos de los documentos originales.** La IA debe:

- Respetar la clasificación del documento tal como está declarada.
- Si no tiene autorización para un documento, o el documento no está disponible para ella, **debe decirlo explícitamente** — nunca inferir, reconstruir o completar su contenido a partir de fragmentos indirectos.
- No asumir que el hecho de que una persona esté conversando con la IA le otorga automáticamente el nivel de acceso de Dirección.

Esta regla es de comportamiento de la IA (Capa 2) y debe reflejarse también en `SKILL.md`, no solo aquí.

## 6. Responsables de validación de clasificación (propuesta inicial)

| Rol | Responsabilidad |
|---|---|
| Dirección | Autoridad máxima de clasificación y autorización |
| Responsable de cada área (cuando exista) | Administra el acceso de su documentación |
| Jurídico | Valida la clasificación de asuntos legales |
| Contabilidad | Valida la clasificación financiera |
| Recursos Humanos | Valida la clasificación de datos laborales/personales |
| Ingeniería | Valida la clasificación de información técnica propietaria |

No se nombran personas concretas en este documento — eso corresponde a la matriz de accesos, que **todavía no existe** (ver §7). No se fabrican responsables que no han sido formalmente designados.

## 7. Matriz de accesos

**PENDIENTE DE IMPLEMENTACIÓN.** La matriz real de personas/cuentas con acceso CONFIDENCIAL y RESTRINGIDO por área se construirá cuando se defina la configuración técnica de GitHub + Google Drive + Claude (ver `01_ARQUITECTURA_MAESTRA.md` §10). Mientras no exista matriz formal, **Dirección (Douglas Castillo) es el punto de autorización por defecto para cualquier acceso a CONFIDENCIAL o RESTRINGIDO.**

## 8. Regla de clasificación por defecto ante duda

Ante duda sobre el nivel de un documento nuevo, se clasifica en el nivel **más restrictivo de los aplicables** hasta que Dirección o el profesional competente confirme que puede bajarse.

## 9. Revisión de esta clasificación

**PENDIENTE DE APROBACIÓN:** periodicidad de revisión de los niveles de confidencialidad en sí (no de los accesos, que se audita según `03_REGLAS_VERSIONAMIENTO.md` / `05_HISTORICO_DECISIONES_GOBIERNO.md`). Se sugiere revisión anual o ante cambio normativo relevante, sujeto a decisión de Dirección.
