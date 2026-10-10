# LV-ING-REF-002 — Análisis de ficha técnica: Sistema batiente Línea Superior Serie 35

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-002  
**Versión:** 0.2  
**Fecha:** 2026-10-10  
**Estado:** BORRADOR — POR VALIDAR  
**Responsable:** Dirección General (Douglas Castillo)  
**Aprobador:** Dirección General  

---

# 1. PROPÓSITO

Analizar la ficha técnica de un sistema completo y convertirla en datos que el agente cotizador pueda usar para **verificar, despiezar y cotizar** sin intervención humana. Es el modelo para cargar las demás series (33, 50, 80, Koncept 40 a 100).

**Fuente:** `ficha-tec-serie-35---PROYECTANTE.pdf`, revisión 01 - 20180410. Google Drive › 01. LA VENTANERÍA INGENIERÍA & DISEÑO › Fichas Técnicas.

**Datos para el agente:** `COTIZADOR_AGENTE/src/cotizador_agente/datos/sistemas/superior_serie_35.json`

---

# 2. QUÉ ES EL SISTEMA

- Sistema **batiente** con marco de 35 mm: puertas batientes, ventanas proyectantes y vidrios fijos.
- Cortes a 45° en marco y naves, ensamble con escuadras de botón.
- Vidrios monolíticos y laminados de **4 a 10 mm**.
- Cierre monopunto, doble sello con empaques EPDM, drenaje mejorado.
- El fabricante declara el sistema "calculado para NSR-10" según sus tablas de restricciones.

---

# 3. LO QUE TRAE LA FICHA Y CÓMO LO USA EL AGENTE

| Capítulo de la ficha | Contenido | Uso en el agente |
|---|---|---|
| 1. Características técnicas | Tablas de **presión resistente (kg/m²)** por ancho y alto para fijo OO, proyectante + fijo XO, puerta XX y puerta O/X | Verificar que el sistema resiste la presión de viento de diseño |
| 2. Perfiles | 9 perfiles con referencia, dimensiones e inercias (Ixx, Iyy) | Despiece; verificación de deflexión por Ingeniería |
| 3. Accesorios | Escuadras, manijas, brazos, empaques, calzos, tornillos | Lista de materiales; **selección de brazo** por peso y tamaño de la nave |
| 4. Nudos | Secciones constructivas | Referencia para Ingeniería y Producción |
| 5. Secciones de despiece | **Fórmulas de corte** de perfiles y **descuentos de vidrio** por configuración | Despiece automático |
| 6. Detalles de fabricación | Perforaciones, cajeos y drenajes | Orden de fabricación (fase posterior) |

---

# 4. DESPIECE CARGADO (EJEMPLOS)

**Ventana proyectante X** (A = ancho, H = alto, en mm):

| Perfil | Descripción | Cant. | Corte |
|---|---|---|---|
| 11111034 | Marco tubular horizontal | 2 | A |
| 11111034 | Marco tubular vertical | 2 | H |
| 11122016 | Nave horizontal | 2 | A − 20 |
| 11122016 | Nave vertical | 2 | H − 20 |
| **Vidrio nave** | | 1 | **(A − 112) × (H − 112)** |

**Cuerpo fijo O:** marco 2 × A y 2 × H; pisavidrio 2 × (A − 42) y 2 × (H − 72); **vidrio (A − 52) × (H − 52)**.

También están cargados el **fijo OO con divisor** y la **proyectante + fijo XO**, con sus accesorios. El empaque en U se escoge según el espesor del vidrio: 17196 para 4 a 6 mm, 17197 para 8 mm y 17198 para 9 y 10 mm.

---

# 5. LÍMITES DE LOS BRAZOS PROYECTANTES (CLAVE PARA ESCOGER EL SISTEMA)

| Brazo | Peso máx. | Ancho máx. de nave | Alto máx. de nave |
|---|---|---|---|
| 8" (17491) | 12 kg | 1200 mm | 400 mm |
| 10" (18096) | 14 kg | 1200 mm | 450 mm |
| 12" (17086) | 16 kg | 1200 mm | 550 mm |
| 16" (17116) | 18 kg | 1200 mm | 750 mm |

**Consecuencia:** con apertura horizontal, una nave proyectante de Serie 35 **no puede pasar de 1200 × 750 mm ni de 18 kg**. Ejemplo calculado por el agente para una ventana de 1200 × 750 mm (nave de 1180 × 730): con vidrio de 8 mm pesa 16.4 kg (13.9 de vidrio y 2.5 de aluminio), así que el brazo de 16" sirve; con vidrio de 10 mm pesa 19.9 kg y **ningún brazo sirve**.

---

# 6. HALLAZGOS QUE REQUIEREN DECISIÓN DE INGENIERÍA

1. **La tabla XO llega hasta 2.0 m de altura, pero los brazos limitan la nave a 750 mm.** Probablemente la tabla aplica también al montaje **vertical** (proyectante sobre fijo, O/X), donde la altura H es la del conjunto y no la de la nave. Hay que confirmar cómo leer la tabla antes de que el agente la use para XO lado a lado.
2. **La proyectante sola (X) no tiene tabla de presión propia.** Se propone verificarla con la tabla XO, usando el ancho de nave. Se requiere confirmación.
3. **Celdas vacías en las tablas** (por ejemplo, fijo OO con H = 1.80 m y A > 0.80 m): el agente las trata como **no admisibles**. Debe confirmarse si significan eso o si la presión resistente es menor que la publicada.
4. ~~No trae el peso por metro de los perfiles.~~ **Resuelto:** los pesos salen del Excel `pesos perfiles cotizador.xlsx`: marco nave 11111034 = 0.373 kg/m, marco fijo 11113036 = 0.391, nave ventana 11122016 = 0.661, nave puerta 11123083 = 0.821, zócalo 11125063 = 0.690, divisor 11133080 = 0.702, pisavidrio 11141016 = 0.176, adaptador XX 11181048 = 0.607, mullion 00181033 = 0.170. El agente ya suma vidrio y aluminio para escoger el brazo.
5. **Tablas de puertas XX y O/X:** el texto extraído del PDF quedó desordenado. Se cargan cuando se verifiquen visualmente.
6. **Fecha de la ficha: 2018.** Confirmar con el proveedor que es la revisión vigente.

---

# 7. EJEMPLO DE DICTAMEN DEL AGENTE

Ventana XO de 1600 × 1200 mm (nave 800 + fijo 800), vidrio crudo de 5 mm y presión requerida de 40 kg/m² (valor del cotizador Excel actual):

| Verificación | Resultado | Fuente |
|---|---|---|
| Perfilería | Resiste 298 kg/m² ≥ 40 → **cumple** | Tabla XO de la ficha |
| Vidrio nave 688 × 1088 mm (0.75 m²) | Máx. 9.00 m² → **cumple** | NSR-10 tabla K.4.2-2 |
| Vidrio fijo 748 × 1148 mm (0.86 m²) | Máx. 9.00 m² → **cumple** | NSR-10 tabla K.4.2-2 |
| Brazo proyectante | Nave de 1180 mm de alto > 750 mm → **ningún brazo sirve** | Ficha, capítulo 3 |

**Dictamen: no cumple como XO lado a lado.** El agente propone bajar la altura de la nave (fijo arriba o abajo, configuración O/X) o cambiar a otro sistema. Este es el tipo de criterio técnico que debe aplicar antes de digitar una cotización.

---

# 8. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-10-10 | Creación: análisis de la ficha y carga de datos para el agente |
| 0.2 | 2026-10-10 | Pesos de perfiles cargados; peso de nave con vidrio y aluminio |
