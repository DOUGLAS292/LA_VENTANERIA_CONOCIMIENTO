```
Nombre del documento: Contrato de la API de Cotización (Agente ↔ Motor)
Código: LV-COM-API-001 (provisional, pendiente de asignación oficial)
Versión: 0.1
Fecha: 2026-10-09
Responsable: Dirección General (Douglas Castillo)
Revisor: Sergio (desarrollo de la API)
Aprobador: Dirección General
Estado: Borrador
```

# Contrato de la API de Cotización

## 1. Propósito

Este documento fija **qué le envía el agente a la API y qué le responde la API**. Es el plano compartido entre los dos frentes:

| Frente | Responsable | Alcance |
|---|---|---|
| **Agente cotizador** | La Ventanería (este repositorio) | Conversación, captura y validación de datos, presentación de la cotización |
| **Motor / API de cotización** | Sergio (o cualquier proveedor que cumpla este contrato) | Despiece, materiales, precios, alertas técnicas |

Mientras la API real no exista, el agente trabaja contra un **motor simulado** que cumple este mismo contrato con precios de prueba. Cualquier API que respete este contrato se conecta sin cambiar el agente.

## 2. Principios no negociables

1. **El precio lo calcula siempre la API, nunca el agente.** El agente no envía precios, descuentos ni márgenes.
2. **Toda cotización con alertas de Ingeniería sale como `preliminar`.** Una cotización comercial no constituye aprobación de ingeniería (`05_INGENIERIA/README.md`).
3. **Precios y cifras reales no viven en GitHub.** Los precios reales los administra la API en su propia base de datos (`00_GOBIERNO_CONOCIMIENTO/README.md`).
4. **Medidas siempre en milímetros (mm), valores en pesos colombianos (COP).**

## 3. Conexión

| Elemento | Valor |
|---|---|
| Protocolo | HTTPS, JSON (UTF-8) |
| URL base | La define Sergio. El agente la lee de la variable `COTIZADOR_API_URL` |
| Autenticación | Encabezado `Authorization: Bearer <token>`. El agente lo lee de `COTIZADOR_API_TOKEN` |
| Versionado | Prefijo `/v1/` en todas las rutas |
| Tiempo máximo de respuesta | 10 segundos por solicitud |

## 4. Endpoints

### 4.1 `GET /v1/catalogo`

Devuelve lo que la API sabe cotizar. El agente lo usa para ofrecer solo opciones válidas.

**Respuesta 200:**

```json
{
  "version_precios": "2026-10-01",
  "sistemas": [
    {
      "codigo": "corrediza",
      "nombre": "Ventana corrediza",
      "ancho_min_mm": 600,
      "ancho_max_mm": 3000,
      "alto_min_mm": 600,
      "alto_max_mm": 2400,
      "vidrios_permitidos": ["crudo_5mm", "templado_6mm", "laminado_6mm"],
      "colores_permitidos": ["natural", "blanco", "negro", "madera"]
    }
  ],
  "vidrios": [
    { "codigo": "templado_6mm", "nombre": "Vidrio templado 6 mm" }
  ]
}
```

### 4.2 `POST /v1/cotizaciones`

Calcula una cotización. **No guarda nada en el CRM**: solo calcula.

**Solicitud:**

```json
{
  "referencia_cliente": "Apto 502 - Torre B",
  "ciudad": "Bogotá",
  "items": [
    {
      "sistema": "corrediza",
      "ancho_mm": 1500,
      "alto_mm": 1200,
      "cantidad": 2,
      "vidrio": "templado_6mm",
      "color_perfil": "negro",
      "piso": 8
    }
  ]
}
```

| Campo | Tipo | Regla |
|---|---|---|
| `referencia_cliente` | texto | Obligatorio. Máximo 120 caracteres |
| `ciudad` | texto | Obligatorio. Afecta transporte e instalación |
| `items` | lista | Entre 1 y 50 ítems |
| `items[].sistema` | texto | Debe existir en `/v1/catalogo` |
| `items[].ancho_mm`, `alto_mm` | entero | Dentro de los límites del sistema |
| `items[].cantidad` | entero | Entre 1 y 500 |
| `items[].vidrio` | texto | Debe estar en `vidrios_permitidos` del sistema |
| `items[].color_perfil` | texto | Debe estar en `colores_permitidos` del sistema |
| `items[].piso` | entero | 1 = primer piso. Activa la revisión de carga de viento |

**Respuesta 200:**

```json
{
  "cotizacion_id": "COT-2026-000123",
  "estado": "preliminar",
  "moneda": "COP",
  "version_precios": "2026-10-01",
  "vigencia_dias": 15,
  "items": [
    {
      "indice": 0,
      "descripcion": "Ventana corrediza 1500 x 1200 mm, templado 6 mm, perfil negro",
      "cantidad": 2,
      "precio_unitario": 1250000,
      "subtotal": 2500000,
      "materiales": [
        { "concepto": "Perfilería", "cantidad": 10.8, "unidad": "ml", "valor": 980000 },
        { "concepto": "Vidrio templado 6 mm", "cantidad": 3.6, "unidad": "m2", "valor": 900000 }
      ]
    }
  ],
  "subtotal": 2500000,
  "iva": 475000,
  "total": 2975000,
  "alertas": [
    {
      "codigo": "CARGA_VIENTO",
      "nivel": "ingenieria",
      "indice_item": 0,
      "mensaje": "Instalación en piso 8: requiere verificación de carga de viento por Ingeniería."
    }
  ]
}
```

| Campo | Regla |
|---|---|
| `estado` | `firme` si no hay alertas de nivel `ingenieria`; `preliminar` en caso contrario |
| `alertas[].nivel` | `informativa` (no bloquea) o `ingenieria` (la cotización queda preliminar) |
| `materiales` | Opcional. Si viene, el agente lo muestra solo al asesor, no al cliente final |
| Valores monetarios | Enteros en COP, sin decimales |

### 4.3 Errores

Toda respuesta de error usa este formato:

```json
{
  "error": {
    "codigo": "MEDIDA_FUERA_DE_RANGO",
    "mensaje": "El ancho 3500 mm supera el máximo de 3000 mm para corrediza.",
    "indice_item": 0
  }
}
```

| HTTP | Cuándo |
|---|---|
| 400 | Datos inválidos (`SISTEMA_DESCONOCIDO`, `MEDIDA_FUERA_DE_RANGO`, `VIDRIO_NO_PERMITIDO`, `COLOR_NO_PERMITIDO`, `DATO_FALTANTE`) |
| 401 | Token ausente o inválido |
| 429 | Demasiadas solicitudes |
| 500 | Error interno del motor |

El agente le muestra al usuario el `mensaje` de los errores 400 para que corrija el dato. Los errores 401, 429 y 500 los reporta como falla técnica, sin inventar un precio.

## 5. Pendientes para acordar con Sergio

- [ ] Tecnología y hosting de la API.
- [ ] Lista definitiva de sistemas, vidrios y colores de la versión 1.
- [ ] Reglas de alertas de Ingeniería (áreas máximas por espesor, piso o altura de revisión de viento, vidrio de seguridad obligatorio). **Las define Ingeniería, no el desarrollador.**
- [ ] Inclusión de instalación, transporte y AIU en el precio.
- [ ] Fecha de primera entrega para pruebas.

## 6. Historial

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1 | 2026-10-09 | Borrador inicial para revisión con Sergio |
