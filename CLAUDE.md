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
