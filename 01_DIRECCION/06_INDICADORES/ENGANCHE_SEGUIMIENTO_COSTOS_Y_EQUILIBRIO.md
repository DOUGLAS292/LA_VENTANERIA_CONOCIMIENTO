```
Nombre del documento: Seguimiento de costos y punto de equilibrio de Enganche
Código: LV-DIR-001
Versión: 1.0
Fecha: 2026-11-22
Responsable: Dirección General (Douglas Castillo)
Revisor: —
Aprobador: Dirección General
Estado: Vigente
Clasificación: CONFIDENCIAL (este archivo solo apunta a la hoja; no contiene cifras)
```

# Seguimiento de costos y punto de equilibrio de Enganche

## 1. Qué es

Una hoja de cálculo con los costos mensuales de Enganche, el punto de equilibrio
y un registro de seguimiento cada 15 días. Las cifras viven en la hoja, no en
este repositorio (ver `02_NIVELES_CONFIDENCIALIDAD.md`, información financiera).

- Hoja: https://claude.ai/artifact/H98ubDRrdxHWNyDjTUgdKJ
- Documento de la hoja (para Claude, Claude Docs): `82b50a99-e392-4797-92cb-b600ced86ebd`
- Es privada: solo Douglas puede abrirla mientras no la comparta.

## 2. Pestañas

| Pestaña | Para qué sirve |
|---|---|
| Supuestos | Números de entrada (celdas amarillas): dólar, planes de Vercel y Supabase, dominio, pauta de Meta, SMS, WhatsApp, precio del Urgente, comisiones de Wompi y de Enganche. |
| Costos | Costos mensuales en dólares y pesos, con total sin pauta y total con pauta. |
| Equilibrio | Neto por Urgente, cuántos Urgentes o trabajos cubren los costos, y resultado del mes. |
| Escenarios | Lanzamiento, Crecimiento y "Tu escenario", lado a lado. |
| Seguimiento | Una fila por revisión: usuarios, registros, publicaciones, postulaciones, Urgentes pagados, SMS, avisos activados, gasto real de pauta, costo por registro y saldo de otp.com. |

## 3. Revisión cada 15 días

- Frecuencia: los días 7 y 22 de cada mes, a las 2:47 p. m. (hora de Colombia).
- Primera revisión programada: 7 de diciembre de 2026.
- Responsable de alimentarla: Claude, con los datos de la base de datos (Supabase,
  proyecto de Enganche) y de Vercel. Douglas aporta lo que solo él ve: el gasto real
  de la pauta de Meta, el saldo de otp.com y las facturas de Vercel y Supabase.
- Cada revisión: agregar una fila en `Seguimiento`, actualizar `Supuestos` con
  valores reales, revisar `Equilibrio` y `Escenarios`, y dar a Douglas una
  recomendación corta (seguir, subir o bajar la pauta; recargar saldo; ajustar precios).

## 4. Reglas

- Los supuestos que no son datos reales (dólar, comisión de Wompi, costo de WhatsApp,
  Urgentes y trabajos de ejemplo) se marcan como tales hasta que se confirmen.
- Los pagos y datos de usuarios se reportan agregados y con celulares enmascarados.
- Este archivo no debe incluir cifras de la hoja ni datos personales.
