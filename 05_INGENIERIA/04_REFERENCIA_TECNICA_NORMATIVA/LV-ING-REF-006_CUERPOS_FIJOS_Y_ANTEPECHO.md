# LV-ING-REF-006 — Cuerpos fijos y antepecho: distribución vertical del vano

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-006  
**Versión:** 1.2  
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

# 5. PERFILES DE LOS FIJOS: SISTEMA S3831 DE ALÚMINA

Para los fijos superiores e inferiores, y para vitrinas, el agente verifica los perfiles con las tablas TR-S3831.

| Elemento | Opciones, de la más liviana a la más pesada | Cómo se lee la tabla |
|---|---|---|
| Vertical (paral) | DIVISB0292 → JAMBAB0174 + ADAPTA0175 → reforzado con ADAPT1859 | Ancho del módulo y altura del vertical |
| Horizontal (travesaño) | DIVISB0292 → JAMBAB0174 + ADAPTA0175 → reforzado con ADAPT1859 | Longitud del horizontal y altura del módulo |

**Ejemplo.** Una vitrina con módulos de 1.20 m de ancho y verticales de 1.20 m de alto, en un edificio de 30 m en Barranquilla (presión de unos 170 kg/m²):

- El divisor sencillo resiste 86 kg/m² y no alcanza.
- El paral JAMBAB0174 + ADAPTA0175 resiste 131 kg/m² y tampoco alcanza.
- El paral reforzado con ADAPT1859 resiste 193 kg/m² y sí alcanza.

**Observaciones de la ficha:**

1. En los verticales TR-02 y TR-03, la última columna, desde módulos de 1.60 m, dice "solo divisiones internas". El agente no la usa en fachada.
2. En la TR-02 hay 6 valores, en módulos de 2.20 a 2.40 m, que suben respecto a anchos menores. El agente toma el valor menor vecino.
3. Las tablas de horizontales se cruzan entre sí, porque cada perfil trabaja con un criterio de deflexión distinto. El agente revisa cada perfil en su propia tabla y no asume un orden.

# 6. PREGUNTAS DEL AGENTE AL CLIENTE

1. Ancho y alto del vano libre, sin contar el muro.
2. Altura del muro o antepecho desde el piso terminado.
3. Piso donde queda la ventana, y si al otro lado hay un desnivel de 1 m o más.
4. Si desea cuerpo fijo inferior.
5. Si desea cuerpo fijo superior, y de qué alto.
6. Tipo de edificación.

---

# 7. PENDIENTES

| # | Pendiente | Responsable |
|---|---|---|
| 1 | Verificar el travesaño (divisor u horizontal de unión) con la tabla de cada serie. Cargadas: Koncept 40, Koncept 50, Serie 35, Koncept 70 (unión puerta con fijo superior) y S3831 de Alúmina (verticales y horizontales de fijo). Faltan Koncept 100 (fijos) y Serie 50 (horizontales) | Agente |
| 1b | Koncept 70, unión puerta con fijo superior: la ficha trae 9 celdas donde un horizontal más largo resiste más que uno más corto (largos de 2.20, 2.40 y 2.70 m con alturas de 0.60 a 1.00 m). El agente toma ahí el valor menor vecino. Confirmar | Ingeniería |
| 2 | Zonas exactas de riesgo de impacto de la Figura K.4.3-0 | Ingeniería |

---

# 8. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-10 | Creación con los criterios de Dirección General: travesaño a 1.10 m y vidrio recocido de 5 mm cuando la norma lo permite |
| 1.1 | 2026-10-10 | Koncept 70: tabla del horizontal de unión entre puerta y fijo superior |
| 1.2 | 2026-10-10 | Sistema de cuerpo fijo S3831 de Alúmina: 3 verticales y 3 horizontales |
