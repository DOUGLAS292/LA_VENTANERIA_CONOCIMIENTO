# Instrucciones permanentes para Claude en este proyecto

## Recordatorios de tareas pendientes

Siempre que, en el curso de una conversación, quede algo pendiente por hacer que
dependa de una acción de Douglas (no de Claude) — por ejemplo: un login, una
aprobación, un pago, una decisión, revisar algo en una plataforma externa —
Claude debe crear de inmediato un recordatorio (vía `CronCreate` si está
disponible en la sesión) para avisarle más adelante, sin que Douglas tenga que
pedirlo explícitamente. Esto aplica siempre, en cualquier tema (Enganche, La
Ventanería, o cualquier otro).

Si la tarea es muy inmediata (minutos), no hace falta programar un recordatorio
formal — basta con mencionarlo claramente en la respuesta. Los recordatorios
formales son para cosas que se puedan olvidar entre sesiones o de un día para
otro (ej. "revisar el login mañana", "hacer login de OAuth", "pagar una
factura", "confirmar algo con un tercero").

## Seguimiento de costos de Enganche (instrucción permanente de Douglas)

Claude alimenta siempre la hoja de costos y punto de equilibrio de Enganche
(https://claude.ai/artifact/H98ubDRrdxHWNyDjTUgdKJ, ficha en
`01_DIRECCION/06_INDICADORES/ENGANCHE_SEGUIMIENTO_COSTOS_Y_EQUILIBRIO.md`).
Cada 15 días (días 7 y 22, tarea programada) se agrega una fila en la pestaña
`Seguimiento`, se actualizan los supuestos con valores reales y se le da a Douglas
una recomendación corta. Si cambia un costo (plan, tarifa, pauta, proveedor),
Claude actualiza la hoja en el momento sin que se lo pidan.
