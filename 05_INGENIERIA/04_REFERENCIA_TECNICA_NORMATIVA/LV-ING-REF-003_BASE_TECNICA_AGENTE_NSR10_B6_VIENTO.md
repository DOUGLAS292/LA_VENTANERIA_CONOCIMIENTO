# LV-ING-REF-003 — Base técnica del agente: presión de viento NSR-10 Capítulo B.6

**Área:** 05_INGENIERIA  
**Código:** LV-ING-REF-003  
**Versión:** 0.2  
**Fecha:** 2026-10-10  
**Estado:** BORRADOR — POR VALIDAR  
**Responsable:** Dirección General (Douglas Castillo)  
**Aprobador:** Dirección General  

---

# 1. PROPÓSITO

Documentar cómo calcula el agente cotizador la **presión de viento de diseño** de una ventana o fachada a partir de la ciudad, la altura del edificio y la exposición, según el Capítulo B.6 de la NSR-10.

**Fuente:** `2titulo-b-nsr-100 (1).pdf`, Google Drive › 02. INGENIERÍA › 01. Normativa y Reglamentos.  
**Datos para el agente:** `COTIZADOR_AGENTE/src/cotizador_agente/datos/nsr10_b6_viento.json`  
**Cálculo:** `COTIZADOR_AGENTE/src/cotizador_agente/viento.py`

---

# 2. MAPA EÓLICO DE COLOMBIA (FIGURA B.6.4-1)

| Región | Velocidad básica V |
|---|---|
| 1 | 17 m/s (60 km/h) |
| 2 | 22 m/s (80 km/h) |
| 3 | 28 m/s (100 km/h) |
| 4 | 33 m/s (120 km/h) |
| 5 | 36 m/s (130 km/h) |

Zonas no estudiadas (Amazonía y sur de la Orinoquía): la norma ordena usar 28 m/s.

**Ciudades (lectura visual preliminar, criterio conservador):**

| Región | Ciudades |
|---|---|
| 5 | Barranquilla, Cartagena*, Santa Marta*, San Andrés |
| 4 | Riohacha*, Valledupar*, Sincelejo*, Medellín*, Villavicencio*, Yopal*, Neiva* |
| 3 | Montería, Cúcuta*, Bucaramanga*, Ibagué, Bogotá*, Cali*, Popayán*, Pasto, Florencia*, Arauca |
| 2 | Manizales*, Pereira*, Armenia*, Tunja* |
| 1 | Quibdó |

\* Ciudad sobre o junto a una frontera entre regiones: se asignó la **región mayor**. **Ingeniería debe confirmar cada ciudad** con el mapa oficial a mayor escala antes del uso comercial.

---

# 3. MÉTODO DE CÁLCULO

## 3.1 Edificios de hasta 18 m — Método 1 simplificado (B.6.4.2.2)

**pnet = λ · Kzt · I · pnet10**, con un mínimo de **0.40 kN/m²** (B.6.4.2.2.1).

- **pnet10:** figura B.6.4-3, muros. Zona 4 es el interior del muro y zona 5 las franjas de esquina. Depende de la velocidad V y del área efectiva (1, 2, 5, 10 y 50 m²).
- **λ:** factor por altura y exposición (figura B.6.4-2). Va de 1.00 a 1.87.
- **Kzt:** factor topográfico. Vale 1.0 salvo colinas o escarpes, que se escalan a Ingeniería.
- **I:** factor de importancia (tabla B.6.5-1).

## 3.2 Edificios de más de 18 m — Método 2 analítico (B.6.5.12.4.2)

**qh = 0.613 · Kz · Kzt · Kd · V² · I** (en N/m²) y **p = qh · (GCp − GCpi)**.

- **Kz:** tabla B.6.5-3, caso 1, a la altura del edificio. Por criterio conservador se aplica a todo el muro.
- **Kd = 0.85** (tabla B.6.5-4).
- **GCp:** figura B.6.5-14, leída del gráfico. Positivo +0.9 a +0.6; zona 4: −0.9 a −0.7; zona 5: −1.8 a −1.0, entre 2 y 50 m².
- **GCpi = ±0.18:** edificio cerrado (figura B.6.5-2).

## 3.3 Exposición del terreno (B.6.5.6)

| Exposición | Cuándo aplica |
|---|---|
| **B** | Zona urbana o suburbana con edificaciones cercanas, en al menos 800 m (o 20 veces la altura) en dirección al viento |
| **C** | Terreno abierto con pocas obstrucciones. Es la opción por defecto cuando no aplican B ni D |
| **D** | Superficies planas sin obstrucción y **frente al agua** (mar, ciénagas, salinas), en más de 1500 m |

En zona de transición se usa la exposición más desfavorable.

## 3.4 Criterios conservadores del agente

- Área efectiva entre dos valores de la tabla: se usa el **área menor** (nota 4 de la figura B.6.4-3).
- Altura entre dos valores: se usa la **altura mayor**.
- Sin ubicación de la ventana en la fachada: se usa la **zona 5 (esquina)**.
- Exposición por defecto **C**: la norma la aplica siempre que no se demuestre B ni D (B.6.5.6.3).
- Presión mínima de **0.40 kN/m²** en ambos métodos (B.6.1.3.2).
- En edificios de más de 18 m, la presión **nunca es menor que la del Método 1 a 18 m**. Criterio propio de La Ventanería: evita que la presión baje al cambiar de método. Pendiente de aprobación.
- **I = 1.00** mientras no se confirme el grupo de uso. La tabla B.6.5-1 asigna 0.87 al Grupo I (ocupación normal); el agente no aplica esa reducción hasta que Ingeniería lo apruebe.

---

# 4. VALIDACIÓN CONTRA EL COTIZADOR EXCEL

El cotizador Excel actual usa **región 3 y presión requerida de 40 kg/m²**. Para una casa baja en región 3, exposición B, ventana de 1 m² en zona interior, el agente obtiene: pnet10 = 0.36 kN/m², que sube al mínimo de 0.40 kN/m² ≈ **40.8 kg/m²**. **Coincide con el Excel.**

Ejemplos con una ventana de 1.5 m² en zona de esquina:

| Ciudad | Altura del edificio | Región | Presión de diseño |
|---|---|---|---|
| Cali | 6 m | 3 | ≈ 46 kg/m² |
| Bogotá | 12 m | 3 | ≈ 50 kg/m² |
| Barranquilla | 30 m | 5 | ≈ 134 kg/m² |
| Medellín | 60 m | 4 | ≈ 137 kg/m² |

---

# 5. VALIDACIÓN CONTRA LA TABLA DE RESTRICCIONES DE ALÚMINA (VC744)

Fuente: `Buga-Tabla de restricciones -744-R00.pdf` (Grupo Alúmina, "presiones de viento según NSR-10", zona 4), en Drive › Fichas Técnicas.

| Ciudad | Altura | Alúmina VC744 (kg/m²) | Agente, exposición B (kg/m²) | Agente, exposición C por defecto (kg/m²) |
|---|---|---|---|---|
| Bogotá | 3 m | 40 | 41 | 44 |
| Cali | 3 m | 40 | 41 | 44 |
| Medellín | 3 m | 51 | 53 | 64 |
| Barranquilla | 3 m | 62 | 62 | 75 |
| Medellín | 40 m | 96 | — | 86 |
| Barranquilla | 40 m | 116 | — | 101 |

**Conclusiones:**

1. A baja altura y con exposición B, el agente **reproduce la tabla de Alúmina** (40 / 40 / 62 kg/m²). Esto confirma la lectura de las regiones 3 y 5 y de las tablas pnet10.
2. En altura, Alúmina da valores mayores en Medellín y Barranquilla. Probablemente usa exposición D en la costa o hipótesis más severas de coeficientes. **Regla del agente: cuando exista tabla del fabricante para la ciudad, usa el mayor valor entre la NSR-10 calculada y la tabla del fabricante.**
3. En Bogotá, Alúmina mantiene 40 kg/m² hasta 30 m, mientras que Cali sube. Indica que **Bogotá podría estar en la región 2**; el agente la mantiene en la región 3 (conservador) hasta que Ingeniería decida.
4. Alúmina indica incrementar un **35% en zona de esquina** (zona 5). El agente usa directamente las tablas de zona 5 de la norma.

---

# 6. PENDIENTES

| # | Pendiente | Responsable |
|---|---|---|
| 1 | Confirmar la región de cada ciudad marcada con * | Ingeniería |
| 2 | Decidir si se aplica I = 0.87 a vivienda (Grupo I) | Ingeniería |
| 3 | Confirmar los valores de GCp leídos del gráfico de la figura B.6.5-14 | Ingeniería |
| 4 | Confirmar Kz de exposición C a 36.5 m (el PDF repite 1.36) | Ingeniería |
| 5 | Edificios irregulares, con efectos topográficos (Kzt > 1) o de más de 152 m: fuera del alcance del agente | — |

---

# 7. HISTORIAL

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-10-10 | Creación a partir del Título B de la NSR-10 cargado en Drive |
| 0.2 | 2026-10-10 | Exposición C por defecto, mínimo 0.40 kN/m² en Método 2 y validación contra la tabla Alúmina VC744 |
