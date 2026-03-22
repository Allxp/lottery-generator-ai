SKILL_STATS_BRAIN.md: Cerebro Estadístico y Bucle de Aprendizaje
Este archivo de Skill define la lógica matemática, los criterios de ranking y el flujo de autoevaluación para la legión de agentes [23, Conversación].
1. Dimensiones de la Habilidad (Metadata)
What: Núcleo de cálculo probabilístico, asignación de ranking y backtesting dinámico [Conversación].
Why: Los humanos eligen patrones predecibles (fechas, secuencias); la IA debe optimizar la "originalidad" y aprender de la tómbola real para reducir la probabilidad de compartir premios
.
Where: Se activa al ejecutar tareas en engines/stats, models/ranking o cuando el spec.md solicita "generación inteligente" [Conversación].
Learned: La carga modular evita el context bloat, permitiendo procesar matrices complejas sin alucinar con reglas de otros sorteos [23, 25, Conversación].

--------------------------------------------------------------------------------
2. Matrices y Constraints de Dominio
El agente debe aplicar rigurosamente las reglas de validación según el sorteo identificado:
Euromillones: 5 números (1–50) + 2 estrellas (1–12)
.
Loto Dominicano: 6 números (1–40) + 1 Bono (1–12) + 1 SuperBono (1–15). Validación de Era: Al analizar el histórico desde 2010, los campos nulos de bombos antiguos no deben promediarse como ceros para no sesgar las frecuencias actuales [32, 231, Conversación].
La Primitiva: 6 números (1–49) + 1 Reintegro (0–9). Prohibición: El Complementario es de comprobación externa y no debe ser elegido ni generado [151, Conversación].
Bonoloto: 6 números (1–49) con análisis de frecuencia diaria
.

--------------------------------------------------------------------------------
3. Lógica del Ranking Inteligente (Score 1–100)
Cada combinación generada debe recibir una puntuación basada en los siguientes pilares
:
Balance Par/Impar: Priorizar distribuciones equilibradas (ej. 3P/3I) para evitar sesgos extremos
.
Distribución de Rango: Analizar la dispersión entre números bajos y altos según la matriz del juego
.
Rareza y Anti-Patrones: Penalizar secuencias aritméticas y combinaciones basadas en patrones visuales o fechas
.
Originalidad Histórica:
Comparar contra archivos .csv históricos [Conversación].
Política de Etiquetado: No excluir ganadores previos, sino marcarlos como "Ganadora Previa" con su fecha histórica [Conversación].

--------------------------------------------------------------------------------
4. Algoritmo del Bucle de Aprendizaje (Backtesting)
El agente debe autoevaluar su precisión tras cada sorteo oficial siguiendo este flujo [189, Conversación]:
Ingesta y Comparación: Leer el nuevo resultado ganador y compararlo con las 20 mejores predicciones (Top Ranking) generadas para esa fecha [Conversación].
Análisis de Desviación: Si el resultado real muestra tendencias no previstas (ej. predominancia de números fríos), el sistema debe registrar el error de tendencia [Conversación].
Recalibración de Pesos: Ajustar dinámicamente los parámetros de "rareza" y "frecuencia" en el cerebro estadístico para las siguientes ejecuciones [Conversación].
Memoria Engram: Los ajustes realizados deben persistir en el sistema de memoria para evitar la amnesia entre sesiones y mejorar con cada run [22, 27, Conversación].

--------------------------------------------------------------------------------
5. Estándares de Salida y Generación
Consistencia: Los números deben presentarse siempre en un array ordenado ascendentemente [32, Conversación].
Contrato de Resultado: La salida del agente debe ser un JSON estructurado que incluya el score, la etiqueta_historica y la explicación_de_rareza [26, 271, Conversación].