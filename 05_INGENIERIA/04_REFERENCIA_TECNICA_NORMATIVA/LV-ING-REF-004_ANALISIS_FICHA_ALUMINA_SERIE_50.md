# LV-ING-REF-004 — Análisis de ficha técnica: Sistema corredizo Serie 50 (Alúmina)

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-004  
**Versión:** 0.1  
**Fecha:** 2026-10-10  
**Estado:** BORRADOR — POR VALIDAR  
**Responsable:** Dirección General (Douglas Castillo)  
**Aprobador:** Dirección General  

---

# 1. PROPÓSITO

Cargar en el agente cotizador la Serie 50 corrediza, que es el sistema que usa hoy el cotizador Excel de La Ventanería, empezando por lo que define la seguridad del producto: **la selección del enganche según la presión de viento**.

**Fuente:** `FICHA-TECNICA-SERIE-50-R05-220513.pdf`, revisión 05 - 220513. Google Drive › Fichas Técnicas.  
**Datos para el agente:** `COTIZADOR_AGENTE/src/cotizador_agente/datos/sistemas/alumina_serie_50.json`

---

# 2. EL SISTEMA

- Ventanas y puertas corredizas y cuerpos fijos: XX, XO, XOX, OXXO, XXX.
- Cortes a 90° y ensamble con tornillos. Marco de 53 mm de profundidad. Aluminio AA6063 T5.
- Vidrios monolíticos y laminados de 4 a 10 mm.
- Rodamientos de 40 kg por nave en ventana y de 80 kg por nave en puerta.
- Tres enganches: **ENGAN2220** (sencillo), **ENGAN2221** (semirreforzado) y **ENGAN2222** (reforzado), que se combinan según el viento.

---

# 3. CÓMO ESCOGE EL ENGANCHE EL AGENTE

El cálculo es el mismo que el "juego recomendado" del cotizador Excel:

1. Calcula la presión de diseño de la obra con la NSR-10 (LV-ING-REF-003).
2. Recorre las 6 combinaciones de enganche **de la más liviana a la más resistente**: sencillo → sencillo + semirreforzado → semirreforzados → sencillo + reforzado → semirreforzado + reforzado → reforzados.
3. Escoge la **primera** cuya presión resistente (tabla de la ficha, con el ancho de la nave y la altura del sistema) sea mayor o igual a la de diseño.
4. Si ninguna resiste, no cotiza ese sistema: lo escala a Ingeniería o propone naves más angostas u otro sistema.

Para OXXO, el cierre central se escoge igual entre el cierre medio semirreforzado (ADAPT2224) y el reforzado (ADAPT2223).

**Ejemplos (pruebas automáticas del agente):**

| Caso | Presión | Enganche escogido | Resiste |
|---|---|---|---|
| Ventana de 1.20 m de alto, naves de 0.80 m | 40 kg/m² | Sencillos | 61 kg/m² |
| Ventana de 1.50 m de alto, naves de 0.80 m | 60 kg/m² | Sencillo + semirreforzado | 134 kg/m² |
| Puerta de 2.40 m, naves de 1.20 m (costa, en altura) | 100 kg/m² | Reforzados | 113 kg/m² |
| Puerta de 2.60 m, naves de 1.20 m | 120 kg/m² | **Ninguno**: se escala | — |

---

# 4. CONTROL DE CALIDAD DE LA EXTRACCIÓN

Varias filas de las tablas venían desordenadas en el texto del PDF y se reconstruyeron. Como control, el agente verifica que **todas** las tablas sean decrecientes al aumentar el ancho y la altura, como corresponde físicamente. Todas lo son. Aun así, la verificación visual por Ingeniería queda pendiente.

---

# 5. PENDIENTES

| # | Pendiente |
|---|---|
| 1 | Fórmulas de corte de los perfiles: en la ficha están como imagen. Se cargarán desde el cotizador Excel o por verificación visual |
| 2 | Descuentos de vidrio de cada configuración, con su rótulo |
| 3 | Tablas de presión por el horizontal del cuerpo fijo |
| 4 | Verificación visual de las tablas reconstruidas |

---

# 6. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-10-10 | Creación: tablas de enganche y cierre medio, selector automático |
