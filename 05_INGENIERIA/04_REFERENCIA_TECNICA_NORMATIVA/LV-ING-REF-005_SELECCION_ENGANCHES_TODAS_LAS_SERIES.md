# LV-ING-REF-005 — Selección de enganches por viento en todas las series corredizas

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-005  
**Versión:** 1.0  
**Fecha:** 2026-10-10  
**Estado:** APROBADO — Dirección General, 2026-10-10. Fichas y normas fuente validadas por Ingeniería  
**Responsable:** Dirección General (Douglas Castillo)  
**Aprobador:** Dirección General  

---

# 1. PROPÓSITO

Dejar en el agente cotizador las tablas de presión resistente de los enganches y cierres centrales de cada serie corrediza, para que escoja la combinación correcta según:

- las medidas: ancho de la nave y altura del sistema;
- la presión de viento de la obra, calculada con la NSR-10 por ciudad y altura del edificio (LV-ING-REF-003).

El método es el mismo de la Serie 50 (LV-ING-REF-004): las combinaciones van de la menos a la más resistente, y el agente toma **la primera que resiste**. Si ninguna resiste, no cotiza ese sistema: escala a Ingeniería o propone naves más angostas u otra serie.

---

# 2. SERIES CARGADAS

| Serie | Archivo del agente | Enganches, de menor a mayor resistencia | Cierre central OXXO |
|---|---|---|---|
| Serie 33 (Alúmina) | `alumina_serie_33.json` | ENGAN1968 con ENGAN1964 → ENGAN1965 → ENGAN1966 | 1 tabla, perfil por confirmar |
| Serie 50 (Alúmina) | `alumina_serie_50.json` | 6 combinaciones de ENGAN2220 / 2221 / 2222 | ADAPT2224 → ADAPT2223 |
| Serie 80 (Alúmina) | `alumina_serie_80.json` | 2282+2282 → 2282+2249 → 2249+2249 → 2282+2250 → 2249+2250 → 2250+2250 | ADAPT2266 → ADAPT2265, con TRASL2247 |
| Koncept 50 | `koncept_50.json` | Un solo enganche: ADAPT1927 | ADAPT2018; además divisor fijo DIVIS1702 |

**Hallazgo de la Serie 80.** El orden real de resistencia **no** es el que sugiere el nombre de los perfiles. Por ejemplo, ENGAN2249 solo (los dos enganches iguales) resiste **menos** que la combinación ENGAN2282 + ENGAN2250. El agente usa el orden comprobado contra las tablas.

---

# 3. CONTROL DE CALIDAD (PRUEBAS AUTOMÁTICAS)

Para cada serie, el agente comprueba en cada tabla:

1. **Monotonía:** la resistencia baja al crecer el ancho de la nave o la altura.
2. **Orden:** cada combinación resiste al menos lo de la anterior en todas las alturas comunes.

Las cuatro series pasan los dos controles. Las fichas fuente están validadas por Ingeniería (Dirección General, 2026-10-10).

---

# 4. EJEMPLOS: QUÉ ESCOGE EL AGENTE

Presión de diseño NSR-10 con exposición C y zona de esquina (valores por defecto del agente). Cada celda muestra la presión de diseño en kg/m², el enganche escogido y, entre paréntesis, lo que resiste.

| Producto | Bogotá, casa (6 m) | Bogotá, edificio (30 m) | Medellín, casa | Medellín, edificio | Barranquilla, casa | Barranquilla, edificio |
|---|---|---|---|---|---|---|
| Serie 33: ventana 1.20 × 1.20, naves de 0.60 | 59 → 1968+1965 (96) | 104 → 1968+1966 (170) | 84 → 1968+1965 (96) | 144 → 1968+1966 (170) | 99 → 1968+1966 (170) | 171 → **no resiste** |
| Koncept 50: ventana 1.60 × 1.20, naves de 0.80 | 59 → ADAPT1927 (94) | 104 → **no resiste** | 84 → ADAPT1927 (94) | 144 → **no resiste** | 99 → **no resiste** | 171 → **no resiste** |
| Serie 50: ventana 2.00 × 1.50, naves de 1.00 | 59 → sencillo + semirreforzado (115) | 104 → sencillo + semirreforzado (115) | 84 → sencillo + semirreforzado (115) | 144 → semirreforzados (204) | 99 → sencillo + semirreforzado (115) | 171 → semirreforzados (204) |
| Serie 80: puerta 2.40 × 2.40, naves de 1.20 | 54 → 2282+2249 (55) | 99 → 2282+2250 (205) | 79 → 2249+2249 (91) | 137 → 2282+2250 (205) | 92 → 2282+2250 (205) | 163 → 2282+2250 (205) |

**Lectura de ingeniería:**

- Las series livianas (Serie 33 y Koncept 50) sirven en casas y edificios bajos del interior. En la costa o en altura, el agente pasa a la Serie 50 o a la Serie 80.
- En Bogotá en altura, el agente da presiones mayores que la tabla de Alúmina (40 kg/m²), porque mantiene Bogotá en región 3 y usa exposición C por defecto. Si Ingeniería confirma región 2 o exposición B, el agente escogerá enganches más livianos y la oferta será más competitiva.

---

# 5. PENDIENTES

| # | Pendiente | Responsable |
|---|---|---|
| 1 | Contrastar la transcripción contra el PDF en las primeras obras cotizadas (las fichas fuente ya están validadas) | Ingeniería |
| 2 | Serie 33: identificar el perfil del cierre central OXXO (página 1-6) | Ingeniería |
| 3 | Koncept 50: tabla de ventana sobre cuerpo fijo (página 1-6). No se sabe qué medida va en filas y cuál en columnas; el agente no la usa | Ingeniería |
| 4 | Koncept 40, 70, 90 y 100: los PDF superan el tamaño que el conector de Drive permite descargar. Opciones: subirlos divididos por páginas, o reconstruir las tablas desde el texto | Douglas / agente |
| 5 | Koncept 55 (plegable) y VC S35: el texto no trae tablas de presión legibles; revisar si están como imagen | Agente / Ingeniería |
| 6 | Fichas TR de Alúmina (8025, 7038, S3831, 744): cargar sus tablas de restricción | Agente |
| 7 | Fórmulas de corte y descuentos de vidrio por serie | Agente |

---

# 6. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-10-10 | Creación: Serie 33, Serie 80 y Koncept 50 con selección automática; controles de monotonía y orden en las cuatro series |
| 1.0 | 2026-10-10 | Aprobado por Dirección General: fichas y normas fuente validadas por Ingeniería |
