# Agente conversacional cotizador

**Código:** `src/cotizador_agente/agente.py` (conversación) y `src/cotizador_agente/herramientas.py` (cálculos)
**Modelo de IA:** Claude Opus 5.5 (`claude-opus-5-5`)

## Qué hace

1. Conversa con el cliente y le pregunta, pocos datos a la vez:
   - ciudad y piso;
   - producto y configuración;
   - levantamiento del vano (muro, desnivel, fijos);
   - color, vidrio y cantidad.
2. Verifica cada decisión técnica con las herramientas. La IA no calcula: llama al cálculo determinístico y explica el resultado citando la norma.
3. Propone la serie, la configuración, el enganche o la unión, la distribución del vano y el vidrio de cada paño.
4. Cuando el cliente confirma, envía la solicitud al software de cotización.
5. Con la respuesta del software, genera el PDF de la cotización para el cliente.

**Lo que NO hace:** despiece, cortes y precios. Los hace el software de cotización integrado (decisión de Dirección General, 2026-10-13).

## Herramientas

| Herramienta | Qué resuelve | Fuente |
|---|---|---|
| `presion_viento` | Presión de diseño por ciudad, altura y tamaño de nave. Usa el mayor valor entre la NSR-10 y la tabla de Alúmina | NSR-10 B.6, LV-ING-REF-003 |
| `listar_sistemas` | Series cargadas, su uso y sus grupos de perfiles. Incluye lo que no se maneja (Serie 35 corrediza, Koncept 55) | Fichas técnicas |
| `comparar_series` | Qué series resisten la presión y con qué enganche | LV-ING-REF-005 |
| `verificar_perfil` | Opción más liviana que resiste en una serie: enganche, cierre central, vertical, horizontal o unión | LV-ING-REF-004, 005 y 006 |
| `vidrio_por_viento` | Espesor mínimo de vidrio recocido, templado y laminado | NSR-10 K.4.2 |
| `vidrio_seguridad` | Exigencia de vidrio de seguridad por uso y altura | NSR-10 K.4.3.9 |
| `opciones_vidrio` | Vidrios del catálogo maestro que cumplen la NSR-10 y caben en la serie, filtrados por la preferencia del cliente. Sin precios | `catalogo_vidrios.py`, catálogo en Drive |
| `distribuir_vano` | Fijo inferior, ventana y fijo superior. Travesaño a 1.10 m y recocido ≥ 5 mm bajo el travesaño | NSR-10 K.4.3.9.7, LV-ING-REF-006 |
| `enviar_a_cotizar` | Valida la solicitud y la pasa al motor (API de Sergio, alianza Alúmina u otro) | CONTRATO_API.md |
| `generar_pdf_cotizacion` | PDF para el cliente con los precios del software y la ficha técnica verificada | `pdf_cotizacion.py`, LV-MKT-001 |

Si no hay motor conectado, `enviar_a_cotizar` deja la solicitud validada y lista para enviarse.

## Catálogo de vidrios

El catálogo maestro de vidrios es un Excel en Drive. Lleva precios y proveedores, así que nunca va a GitHub.

- **Ubicación:** se indica con `AgenteCotizador(catalogo_vidrios=ruta)` o con la variable de entorno `LV_CATALOGO_VIDRIOS`.
- **Qué lee el agente:** solo las columnas técnicas (familia, tipo NSR-10, láminas, PVB, cámara, color, prestación y estado). No lee la columna de precio: los precios los pone el motor de cotización.
- **Cómo filtra:**
  1. Parte del espesor mínimo por tipo que da `vidrio_por_viento` y de si `vidrio_seguridad` exige vidrio de seguridad.
  2. Descarta lo que no cabe en el rango de vidrio de la serie (ficha técnica): por ejemplo, Serie 50 de 4 a 10 mm y Serie 80 de 6 a 12 mm.
  3. Aplica la preferencia del cliente: color, acústico o control solar.
- **Excluidos:** los insulados y los blindados van a Ingeniería. Los espejos, los rellenos y los vidrios inactivos no se ofrecen.
- **Sin catálogo:** el agente describe el vidrio por tipo y espesor, y el software lo asigna.

## PDF de la cotización

Cada fuente aporta su parte:

- **Del software de cotización:** precios, IVA, total, vigencia y alertas. El agente nunca escribe ni recalcula valores.
- **Del agente:** por cada ítem, la serie, la configuración, la presión de diseño, los perfiles verificados, la distribución del vano (fijo inferior, ventana y fijo superior con su vidrio) y las normas.
- **Colores:** los de la identidad corporativa (LV-MKT-001).
- **Marca de agua:** las cotizaciones preliminares llevan "PRELIMINAR".

Algunos datos no están en GitHub y se pasan al crear el agente con `Empresa(...)`:

- el logo, la tipografía Gilroy, el NIT, la dirección y las condiciones comerciales;
- sin Gilroy, el PDF usa Helvetica y lo marca como "POR VALIDAR CON MARKETING/DIRECCIÓN".

Los PDF se guardan en `cotizaciones/`. Esa carpeta está fuera de GitHub porque lleva precios.

## Cómo probarlo

```bash
cd COTIZADOR_AGENTE
pip install -e ".[dev]"
export ANTHROPIC_API_KEY=...        # la clave nunca va en GitHub
python -m cotizador_agente          # conversación en la consola
python -m pytest                    # pruebas sin conexión (API simulada)
```

## Controles

- **Respaldo ante rechazos:** si el modelo principal rechaza una petición, la API la pasa a otro modelo (`fallbacks: "default"`).
- **Historial:** el historial de la conversación solo crece, no se edita.
- **Errores de herramienta:** si una herramienta recibe un dato inválido (por ejemplo, un travesaño fuera de 760–1100 mm), el error vuelve al agente para que corrija o pregunte al cliente.
- **Límite de pasos:** máximo 25 llamadas a herramientas por mensaje del cliente.
