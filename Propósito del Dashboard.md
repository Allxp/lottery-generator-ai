. Propósito del Dashboard
El objetivo no es solo dar un número, sino validar la intención de la jugada. Debe explicar visualmente por qué una combinación tiene un ranking alto (ej. "95% original") y cómo se aleja de los patrones comunes elegidos por humanos [266, Conversación previa].
2. Dimensiones de Análisis (El Gráfico de Radar)
La pieza central será un gráfico de radar (araña) que evalúe los 4 pilares definidos en la lógica de ranking [264, Conversación previa]:
Balance (P/I): Qué tan equilibrada es la proporción de números pares e impares.
Dispersión (A/B): Cómo se distribuyen los números entre el rango alto y bajo de la matriz.
Rareza (Anti-Patrones): Nivel de éxito en evitar secuencias aritméticas (ej: 1, 2, 3) o fechas (números < 31)
.
Originalidad: Comparativa contra el histórico de sorteos ganadores [264, Conversación previa].
3. Componentes Visuales Clave
Siguiendo los estándares de SKILL_MOBILE_UI.md, el plan incluye:
Indicador de Score Global: Un anillo de progreso o termómetro que muestre la puntuación de 1 a 100 [264, Conversación previa].
Etiquetado Histórico Dinámico: Un badge prominente que identifique la jugada como "Original" o "Ganadora Previa" (incluyendo la fecha exacta en este último caso) [Conversación previa].
Monitor de Aprendizaje: Una pequeña sección de texto o icono que indique si la IA ha ajustado sus pesos recientemente tras un sorteo real (ej: "Ajustado según tendencia del último sorteo de LEIDSA") [Conversación previa].
Selector de Estrategia: En el Modo Experto, controles deslizantes para que el usuario priorice una dimensión sobre otra (ej. sacrificar balance por máxima rareza)
.
4. Reglas de Interacción
Feedback Háptico: Vibración corta al generar una combinación con ranking superior al 90% [Conversación previa].
Validación de Rango: El dashboard debe cambiar sus escalas automáticamente según el sorteo (ej. escala de 1–40 para Loto Dominicano vs 1–50 para Euromillones) [35, 37, Conversación previa].
5. Flujo de Implementación (Plan Mode)
Para que tu legión de agentes construya esto en Google Antigravity:
El Designer presentará un wireframe basado en estos puntos.
El Implementer generará los componentes de gráficas (usando librerías como fl_chart en Flutter).
El Verifier asegurará que los datos del gráfico coincidan exactamente con la salida JSON del SKILL_STATS_BRAIN.md