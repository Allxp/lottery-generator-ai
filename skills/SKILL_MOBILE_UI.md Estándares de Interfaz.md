SKILL_MOBILE_UI.md: Estándares de Interfaz y Experiencia (UI/UX)
Este archivo dota al agente del conocimiento experto para construir la superficie visual de la aplicación en Flutter o React Native, asegurando una experiencia fluida entre el Modo Rápido y el Modo Experto [182, Conversación].
1. Dimensiones de la Habilidad (Metadata)
What: Especialista en diseño de interfaces móviles, visualización de datos estadísticos y flujos de usuario de alto impacto.
Why: Centralizar las reglas de diseño evita que el agente proponga componentes genéricos y asegura que la UI respete las restricciones de cada sorteo (ej. no mostrar complementario en Primitiva) [36, Conversación].
Where: Se activa al trabajar en carpetas de views/, components/, styles/ o al diseñar dashboards visuales.
Context Optimization: El agente solo cargará estas reglas de diseño cuando la tarea sea puramente de frontend, ahorrando tokens de lógica estadística
.

--------------------------------------------------------------------------------
2. Componentes Críticos de Sorteo
El agente debe renderizar los selectores de números adaptándose dinámicamente a la matriz del juego seleccionado:
Grid Dinámico:
Loto Dominicano: 6 slots principales + 1 slot "Más" + 1 slot "Super Más" [Conversación].
Euromillones: 5 slots principales + 2 slots de "Estrellas".
La Primitiva: 6 slots principales + 1 slot de "Reintegro" (Prohibido mostrar selector de complementario) [Conversación].
Etiquetado Histórico: Si el ranking identifica una jugada como "Ganadora Previa", la UI debe mostrar un badge informativo con la fecha del sorteo original, sin bloquear la selección [Conversación].

--------------------------------------------------------------------------------
3. Dashboards de Datos (Visualización)
Siguiendo el spec.md, el agente debe ser capaz de implementar los siguientes elementos visuales
:
Dashboard de Rareza: Uso de gráficos de radar o barras para explicar el Score (1–100) basado en balance par/impar y originalidad [Conversación].
Monitor de Aprendizaje: Una sección visual que indique al usuario cómo los pesos de la IA se han ajustado tras el último sorteo real (ej: "Ajuste de +5% en números calientes") [Conversación].
Indicadores de Estrategia: Termómetros visuales para el nivel de "Riesgo" o "Conservadurismo" en el Modo Experto.

--------------------------------------------------------------------------------
4. Reglas de Interacción y UX
Modo Dual: Implementar un toggle persistente para cambiar entre la Generación 1-Click (Modo Rápido) y los Ajustes Avanzados (Modo Experto)
.
Validación en Tiempo Real: Los campos de entrada deben validar el rango de la tómbola actual (ej: no permitir el número 45 en el Loto Dominicano que llega hasta 40) [Conversación].
Feedback Háptico: Sugerir el uso de vibraciones cortas al generar una combinación con ranking "Top 1%".

--------------------------------------------------------------------------------
5. Estándares de Código Visual
Clean Components: Uso de Atomic Design (Atoms, Molecules, Organisms).
Accesibilidad: Contraste mínimo de 4.5:1 para los números del histórico.
Plan Mode Obligatorio: Antes de escribir CSS o componentes, el agente debe presentar un wireframe en Markdown o una descripción jerárquica para aprobación humana (HITL) [34, Conversación].
