# LV-ING-REF-006 — Cuerpos fijos y antepecho: distribución vertical del vano

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-006  
**Versión:** 1.1  
**Fecha:** 2026-10-10  
**Estado:** APROBADO — Dirección General, 2026-10-10  
**Responsable:** Dirección General (Douglas Castillo)  
**Aprobador:** Dirección General  

---

# 1. PROPÓSITO

Que el agente cotizador pregunte por los cuerpos fijos superior e inferior y calcule, con la NSR-10, cómo se reparte el alto del vano entre el fijo inferior, la ventana y el fijo superior.

**Cálculo:** `COTIZADOR_AGENTE/src/cotizador_agente/vano.py`

---

# 2. LA NORMA (NSR-10 K.4.3.9.7, TABLA K.4.3-7, PÁGINA K-58)

| Situación | Exigencia |
|---|---|
| La ventana protege un desnivel de 1.00 m o más (piso alto, balcón, vacío) | Travesaño o riel de protección entre **0.76 m y 1.10 m** sobre el piso |
| Vidrio debajo del travesaño (tipo B) | Vivienda: vidrio de seguridad, o recocido de mínimo 5 mm según la columna 2 de la Tabla K.4.3-2. Demás edificaciones: columna 3, mínimo 5 mm |
| Vidrio encima del travesaño (tipo C) | Se selecciona por viento, si el travesaño está firmemente asegurado |
| Cualquier vidrio recocido a menos de 0.50 m del piso | Mínimo 5 mm (K.4.3.9.5.1) |

---

# 3. CRITERIOS DE LA VENTANERÍA (DIRECCIÓN GENERAL, 2026-10-10)

1. El travesaño va por defecto a **1.10 m** del piso, el máximo que permite la norma.
2. Debajo del travesaño, el agente usa vidrio **recocido de 5 mm o más cuando la norma lo permite**. Si el área supera la tabla, usa vidrio de seguridad.
3. Un muro o antepecho de **0.76 m o más** ya cumple como protección, así que no se exige fijo inferior. Si el cliente lo quiere de todos modos, se coloca hasta 1.10 m.
4. Si la ventana supera el alto máximo de la serie, el sobrante pasa a fijo superior.

---

# 4. EJEMPLOS

| Caso | Resultado |
|---|---|
| Muro de 0.40 m, vano libre de 2.00 m, piso alto | Fijo inferior de 0.70 m (de 0.40 a 1.10 m) y ventana de 1.30 m |
| Muro de 1.00 m, vano libre de 1.20 m, piso alto | Ventana de 1.20 m, sin fijo exigido. Con fijo pedido por el cliente: fijo de 0.10 m y ventana de 1.10 m |
| Primer piso sin desnivel, vano de 2.10 m desde el piso | Ventana completa, con vidrio de mínimo 5 mm por estar a menos de 0.50 m del piso |
| Muro de 0.40 m, vano de 2.00 m, serie con ventana máxima de 1.10 m | Fijo inferior de 0.70 m, ventana de 1.10 m y fijo superior de 0.20 m |

Vidrio del fijo inferior en vivienda:

- Fijo de 1.50 × 0.70 m (1.05 m²): recocido de 5 mm.
- Fijo de 2.40 × 0.70 m (1.68 m²): recocido de 6 mm en vivienda y de 5 mm en las demás edificaciones.

---

# 5. PREGUNTAS DEL AGENTE AL CLIENTE

1. Ancho y alto del vano libre, sin contar el muro.
2. Altura del muro o antepecho desde el piso terminado.
3. Piso donde queda la ventana, y si al otro lado hay un desnivel de 1 m o más.
4. Si desea cuerpo fijo inferior.
5. Si desea cuerpo fijo superior, y de qué alto.
6. Tipo de edificación.

---

# 6. PENDIENTES

| # | Pendiente | Responsable |
|---|---|---|
| 1 | Verificar el travesaño (divisor u horizontal de unión) con la tabla de cada serie. Cargadas: Koncept 40, Koncept 50, Serie 35 y Koncept 70 (unión puerta con fijo superior). Faltan Koncept 100 (fijos) y Serie 50 (horizontales) | Agente |
| 1b | Koncept 70, unión puerta con fijo superior: la ficha trae 9 celdas donde un horizontal más largo resiste más que uno más corto (largos de 2.20, 2.40 y 2.70 m con alturas de 0.60 a 1.00 m). El agente toma ahí el valor menor vecino. Confirmar | Ingeniería |
| 2 | Zonas exactas de riesgo de impacto de la Figura K.4.3-0 | Ingeniería |

---

# 7. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-10 | Creación con los criterios de Dirección General: travesaño a 1.10 m y vidrio recocido de 5 mm cuando la norma lo permite |
| 1.1 | 2026-10-10 | Koncept 70: tabla del horizontal de unión entre puerta y fijo superior |
