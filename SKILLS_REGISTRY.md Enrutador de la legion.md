SKILLS_REGISTRY.md: Enrutador de la Legión
1. Propósito
Optimizar el rendimiento agéntico mediante la carga selectiva de habilidades bajo demanda. Este registro actúa como el "mapa mental" que el agente consulta antes de actuar para decidir qué reglas específicas de lotería o ingeniería debe integrar en su memoria de trabajo
.
2. Mapa de Habilidades (Skills Map)
Ruta raíz: C:\Users\allxp\Downloads\CURSO DESARROLLO CON IA BRAIS SCHOOL\generador de combinaciones loteria\skills
Dominio
Archivo
Criterio de Carga (Routing)
Loto Dominicano
SKILL_LEIDSA_RULES.md
Tareas sobre LEIDSA o la modalidad SuperMás
.
La Primitiva
SKILL_PRIMITIVA_RULES.md
Tareas sobre Primitiva o validación de Reintegro [Conversación].
Euromillones
SKILL_EUROMILLIONS_RULES.md
Tareas sobre Euromillones o lógica de Estrellas
.
Bonoloto
SKILL_BONOLOTO_RULES.md
Tareas sobre Bonoloto o sorteos de frecuencia diaria
.
Ingeniería de Datos
SKILL_DATA_PIPELINE.md
Actualización de archivos .csv, web scraping o limpieza de nulos
.
Cerebro Estadístico
SKILL_STATS_BRAIN.md
Cálculo de Ranking, backtesting o ajuste dinámico de pesos
.

--------------------------------------------------------------------------------
3. Lógica de Operación (Router)
Detección: El agente analiza la intención del prompt (ej: "actualiza los resultados de LEIDSA")
.
Carga selectiva: El sistema carga los módulos SKILL_DATA_PIPELINE.md y SKILL_LEIDSA_RULES.md, ignorando las reglas de la Primitiva o Euromillones para mantener el contexto limpio
.
Ejecución: El agente opera bajo las instrucciones ultra-específicas del módulo cargado, garantizando que no se mezclen las matrices de números (ej: no usar el rango 1–50 de Euromillones en el Loto Dominicano)
.

--------------------------------------------------------------------------------
4. Persistencia y Aprendizaje (Engram)
Cada vez que una de estas habilidades se utiliza para modificar el código o los datos, el agente debe registrar el resultado en el sistema Engram siguiendo estas cuatro dimensiones para evitar la "amnesia entre sesiones"
:
What: Qué cambio se realizó (ej. actualización de matriz).
Why: Razón del cambio (ej. nuevo sorteo detectado).
Where: Archivos modificados en la ruta del proyecto.
Learned: Ajustes realizados en los pesos del ranking tras el backtesting