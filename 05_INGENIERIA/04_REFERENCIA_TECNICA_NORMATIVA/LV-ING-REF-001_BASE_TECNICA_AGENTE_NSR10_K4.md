# LV-ING-REF-001 — Base técnica del agente: NSR-10 Capítulo K.4 y cargas de viento

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-001  
**Versión:** 0.1  
**Fecha:** 2026-10-10  
**Estado:** BORRADOR — POR VALIDAR  
**Responsable:** Dirección General (Douglas Castillo)  
**Aprobador:** Dirección General  

---

# 1. PROPÓSITO

Definir el conocimiento normativo que usa el **agente cotizador de La Ventanería** para escoger y verificar sistemas vidriados según la NSR-10, y dejar trazable de dónde sale cada dato.

El agente **no calcula ni inventa valores técnicos**. Consulta tablas cargadas en `COTIZADOR_AGENTE/src/cotizador_agente/datos/` y cita el numeral de la norma o la ficha en cada decisión.

---

# 2. FUENTES

| Fuente | Ubicación | Estado |
|---|---|---|
| NSR-10 Título K (PDF oficial, copia IDRD) | Google Drive › Documentos de Ingeniería › `11titulo-k-nsr-100.pdf` | Leído completo el capítulo K.4 |
| NSR-10 Capítulo K.4 (copia ampliada) | Google Drive › `CAPITULO K - REQUISITOS ESPECIALES PARA VIDRIOS...pdf` | No leído (13 MB) |
| Resumen interno NSR-10 para vidrio | Google Drive › 02. INGENIERÍA › 01. Normativa › `NSR-10 - Requisitos aplicables a vidrios y sistemas vidriados` | Leído |
| NSR-10 Título B, capítulo B.6 (viento) | **No está en Drive.** El acceso a la copia pública del IDRD está bloqueado desde el entorno del agente | **FALTA** |
| `requisitos mapa eolico.pdf` | Google Drive | Solo contiene el título; parece un documento escaneado |

---

# 3. CADENA DE VERIFICACIÓN QUE SIGUE EL AGENTE

```
Ciudad + altura + exposición ──► Presión de diseño (Título B, B.6)      [PENDIENTE: falta Título B]
                                        │
          ┌─────────────────────────────┼──────────────────────────────┐
          ▼                             ▼                              ▼
 Perfilería: presión resistente   Vidrio: área máxima por espesor   Seguridad: impacto humano
 de la ficha del sistema ≥        y tipo (tablas K.4.2-2 a 5)        (K.4.3.9) según uso y
 presión de diseño                                                    altura sobre el piso
          └─────────────────────────────┼──────────────────────────────┘
                                        ▼
                    Dictamen: CUMPLE / NO CUMPLE / REQUIERE INGENIERÍA
```

Mientras no esté cargado el Título B, la **presión de diseño entra como dato** (en kg/m²), igual que hoy en el cotizador Excel (`Presión requerida (kg/m2)` y `REGIÓN`).

---

# 4. LO QUE YA SABE EL AGENTE (CAPÍTULO K.4)

## 4.1 Espesor de vidrio por viento (K.4.2.6)

- Tablas K.4.2-2 (recocido), K.4.2-3 (termoendurecido), K.4.2-4 (templado) y K.4.2-5 (laminado con PVB).
- Valen para lámina vertical, **relación largo/ancho ≤ 2** y **apoyada en los cuatro lados**.
- Fuera de esas condiciones el agente no dictamina y escala a Ingeniería (cálculo ASTM E1300-09a, K.4.2.3).
- Criterio conservador: si la presión cae entre dos renglones, usa el renglón de presión mayor.

Ejemplo de la tabla K.4.2-2 (recocido, áreas máximas en m²):

| Presión (kN/m²) | 4 mm | 5 mm | 6 mm | 8 mm | 10 mm |
|---|---|---|---|---|---|
| 0.50 | 6.60 | 9.00 | 12.18 | 19.76 | — |
| 1.00 | 3.03 | 3.92 | 4.99 | 7.22 | 9.59 |
| 2.00 | 1.08 | 1.38 | 1.84 | 2.88 | 3.92 |
| 3.00 | 0.63 | 0.86 | 1.16 | 1.84 | 2.65 |

## 4.2 Vidrio con marco y sin marco

| Caso | Regla | Numeral |
|---|---|---|
| Vidrio recocido **totalmente enmarcado** | Área máxima por espesor (4 mm: 2.0 m²; 5 mm: 3.3; 6 mm: 4.6; 8 mm: 7.0; 10 mm: 9.5). Si el viento supera 1.3 kPa, manda el viento | Tabla K.4.3-3 |
| Vidrio de **seguridad enmarcado** | Templado 4 mm: 2.0 m²; 6 mm: 4.0; 8 mm: 6.0. Laminado 6 mm: 3.0; 8 mm: 5.0; 10 mm: 7.0 | Tabla K.4.3-1 |
| Divisiones internas con **bordes laterales sin marco** | Espesor según altura del vano, uniones a tope y ancho máximo del panel | Tabla K.4.3-4 |
| Vitrinas con **vidrio a tope** | Igual, por altura del vano | Tabla K.4.3-5 |
| Vidrio a tope en radio | Espesor por altura, radio y presión | Tabla K.4.3-6 |
| Puertas con vidrio a tope | Templado mínimo 10 mm | K.4.3.9.2.1(c) |
| Paneles laterales sin marco | Templado mínimo 10 mm | K.4.3.9.3.3.2 |

## 4.3 Vidrio de seguridad obligatorio (K.4.3.9)

- Zona de riesgo de impacto humano: hasta **2000 mm** sobre el piso (figura K.4.3-0).
- Puertas batientes: recocido solo hasta 0.5 m²; por encima, vidrio de seguridad.
- Baños: puertas y divisiones en vidrio de seguridad. Con bordes sin marco, templado de mínimo 5 mm; con bordes adyacentes a tope y en duchas con pivotes o bisagras, de mínimo 6 mm.
- Escuelas y guarderías: vidrio de seguridad hasta 800 mm del piso.
- Barandas enmarcadas: vidrio de seguridad de mínimo 6 mm.
- Escaleras: vidrio de seguridad dentro de 2000 mm del peldaño inferior.
- Vidrio recocido a menos de 500 mm del piso: mínimo 5 mm.
- Pisos de vidrio: laminado de dos o más capas. El templado monolítico no se considera seguro.
- Vidrio de 2 mm prohibido (K.4.2.6.1).

## 4.4 Perfilería

- Deflexión de perfiles que soportan vidrio: **L/175** hasta 4 m; **L/240 + 6.35 mm** entre 4 y 12 m (K.4.2.7.1).
- El agente usa las **tablas de presión resistente de la ficha del fabricante** para verificar la perfilería.

---

# 5. PENDIENTES PARA QUE EL AGENTE CALCULE LA PRESIÓN DE VIENTO

| # | Pendiente | Responsable |
|---|---|---|
| 1 | Subir a Drive (02. INGENIERÍA › 01. Normativa y Reglamentos) el **Título B de la NSR-10** completo, con la figura B.6.4-1 (mapa de amenaza eólica) y el capítulo B.6 | Dirección General |
| 2 | Definir la tabla **ciudad → región eólica** para las ciudades donde trabaja La Ventanería | Ingeniería |
| 3 | Definir el método de presión por altura que usa la empresa (método simplificado o analítico de B.6) y las categorías de exposición | Ingeniería |
| 4 | Verificar visualmente contra el PDF todas las tablas extraídas automáticamente (archivo `nsr10_k4.json`) | Ingeniería |
| 5 | Confirmar los valores dudosos marcados en `nsr10_k4.json` (tabla K.4.3-1, templado 10 mm; tabla K.4.3-2, fila de 3 mm) | Ingeniería |

**Nota sobre el mapa eólico:** las fuentes secundarias consultadas en internet dan valores contradictorios para las velocidades de las regiones 1 a 5. **No se cargó ningún valor de velocidad de viento** hasta tener el Título B oficial.

---

# 6. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-10-10 | Creación: extracción del capítulo K.4 para el agente cotizador |
