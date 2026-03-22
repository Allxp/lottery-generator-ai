SKILL_DATA_PIPELINE.md: Automatización y Normalización de Resultados
Este archivo de Skill dota al agente del conocimiento técnico para orquestar la ingesta, limpieza y actualización de los archivos históricos (.csv), asegurando que el sistema siempre opere con la información más reciente de la Primitiva, Euromillones, Bonoloto y LEIDSA .
1. Dimensiones de la Habilidad (Metadata)
What: Orquestación de tuberías de datos (ETL), validación de matrices y normalización histórica
.
Why: La integridad del Ranking Inteligente depende de datos actualizados; errores en la ingesta (como confundir el Más con el SuperMás) invalidarían las predicciones [159, Conversación].
Where: Se activa al detectar tareas en data/, scripts de actualización o cuando se requiere descargar el último sorteo oficial
.
Trigger: Cada nueva fila añadida al CSV debe disparar automáticamente el Backtesting en la SKILL_STATS_BRAIN.md [Conversación].

--------------------------------------------------------------------------------
2. Protocolo de Actualización Automática (Sources)
El agente debe programar la captura de datos en los siguientes horarios críticos:
Sorteo
Fuente Oficial
Frecuencia / Horario
Matriz de Validación
Bonoloto
SELAE
Diario (21:30 CET)
6 de 49
Euromillones
SELAE
Martes/Viernes (21:15 CET)
5 de 50 + 2 estrellas
La Primitiva
SELAE
Lun/Jue/Sáb (21:40 CET)
6 de 49 + 1 Reintegro [Conversación]
LEIDSA
leidsa.com
Mié/Sáb (20:55 AST)
SuperMás: 6 de 40 + 1 (1–12) + 1 (1–15) [Conversación]

--------------------------------------------------------------------------------
3. Lógica de Normalización de Eras (Caso LEIDSA)
Para evitar alucinaciones estadísticas, el agente debe aplicar estas reglas de Normalización Histórica
:
Identificación de Era: Antes de procesar una fila de historico_loto_leidsa.csv, el agente debe clasificarla:
Era 1: Solo 6 números (columnas Más/SuperMás nulas).
Era 2 (Más): 6 números + 1 número adicional (1–12).
Era 3 (SuperMás): 6 números + 1 adicional (1–12) + 1 adicional (1–15).
Tratamiento de Nulos: Los valores vacíos en registros antiguos no deben tratarse como cero, sino como null para que no afecten el cálculo de frecuencias de los bombos actuales [Conversación].

--------------------------------------------------------------------------------
4. Reglas de Oro de Integridad de Datos
El agente tiene prohibido corromper los archivos históricos. Debe seguir estos pasos:
Deduplicación: Antes de insertar, verificar que la fecha del sorteo no exista en el CSV.
Ascensión: Los 6 números principales deben guardarse siempre en orden ascendente
.
Constraint de Primitiva: El número Complementario debe capturarse en una columna dedicada para comprobación de premios, pero nunca mezclarse con los 6 números de la apuesta [Conversación].
Alerta de Fallo: Si el scraping falla tras 3 intentos, el agente debe notificar al desarrollador y activar el "Modo Manual" definido en el spec.md
.

--------------------------------------------------------------------------------
5. Salida de Datos (Output Format)
Cada registro nuevo debe seguir este estándar de contrato:
{
  "lottery": "leidsa",
  "date": "YYYY-MM-DD",
  "numbers": [n1, n2, n3, n4, n5, n6],
  "additional": [mas, supermas],
  "era_detected": "SuperMas",
  "status": "ready_for_backtesting"
}