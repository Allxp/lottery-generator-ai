# spec.md: Generador Inteligente de Combinaciones de Lotería

## 🧭 Overview
Aplicación móvil de alto rendimiento diseñada para la **generación y optimización estratégica de combinaciones** en sorteos de **La Primitiva, Euromillones, Bonoloto y Loto Dominicano (LEIDSA)** [241, Conversación]. El sistema trasciende el azar simple mediante una **Arquitectura de Orquestación** que combina análisis estadístico masivo, reglas anti-patrones humanos y un **Bucle de Aprendizaje Continuo** basado en resultados reales y comportamiento del usuario [241, 243, Conversación].

---

## 🎯 Alcance Multi-Lotería
El sistema debe cargar contratos de validación y reglas específicas según el sorteo seleccionado:

1.  **Loto Dominicano (LEIDSA):** Generación bajo modalidad **SuperMás** por defecto (6 números del 1–40 + 1 Bono del 1–12 + 1 SuperBono del 1–15). El sistema mantiene conciencia de las 3 eras históricas para evitar sesgos en el análisis de frecuencias [159, Conversación].
2.  **Euromillones:** Selección de 5 números (1–50) y 2 estrellas (1–12) [1].
3.  **La Primitiva:** Selección de 6 números (1–49) y 1 Reintegro (0–9). **Constraint de dominio:** El número Complementario es de comprobación externa y **NO debe ser elegido por el usuario** ni generado en la apuesta [53, Conversación].
4.  **Bonoloto:** Matriz de 6 números (1–49) con frecuencia de sorteo diario [54, Conversación].

---

## 🧠 Motor de Inteligencia y Bucle de Aprendizaje
El núcleo de la aplicación evoluciona mediante dos flujos de retroalimentación (Backtesting):

### 1. Aprendizaje por Resultados (Análisis de Desviación)
*   **Comparación Activa:** Tras cada actualización automática de resultados, el sistema compara el número ganador con las combinaciones de mayor ranking generadas para esa fecha [189, Conversación].
*   **Recalibración de Pesos:** Si la "rareza estadística" predicha se desvía de la realidad de la tómbola, el **Cerebro Estadístico** recalibra automáticamente los parámetros para futuras generaciones [Conversación].
*   **Memoria Engram:** Estos ajustes persisten entre sesiones para resolver la amnesia del agente y mejorar con cada run [22, Conversación].

### 2. Aprendizaje por Comportamiento de Usuario
*   **Selección Activa:** El sistema analiza qué sugerencias del ranking elige el usuario para jugar.
*   **Análisis de Descartes:** Las combinaciones ignoradas penalizan ciertos patrones en el perfil personalizado del usuario [243, Conversación].

---

## 🏆 Ranking Inteligente y Política de Ganadores
Se aplica una **Política de Etiquetado Informativo** en lugar de exclusión [Conversación]:
*   **Inclusión:** El sistema permite generar combinaciones que ya han ganado en el pasado.
*   **Etiquetado Histórico:** Si una combinación generada coincide con el histórico, se marca como **"Ganadora Previa"** indicando su fecha [Conversación].
*   **Puntuación (Score 1–100):** Basada en balance par/impar, distribución de rango, rareza (evitar fechas/secuencias) y originalidad frente a la masa de jugadores.

---

## 📊 Gestión de Datos e Infraestructura
*   **Data Pipeline:** Automatización de la ingesta de resultados desde plataformas oficiales (SELAE y LEIDSA) [64, Conversación].
*   **Normalización de Datos:** Manejo estricto de nulos en registros antiguos para no corromper las frecuencias de los nuevos bombos (Más y SuperMás) [159, Conversación].
*   **Calidad de Producción:** 
    *   **CI/CD:** Pruebas unitarias obligatorias para cada lógica de sorteo [2].
    *   **Security Review:** Auditoría automática con Claude para detectar vulnerabilidades en cada PR [3, 4].
    *   **Release Management:** Uso de **Release Please** para automatizar versiones y notas de lanzamiento con IA [5].

---

## 🎨 UI/UX (Superficie Visual)
*   **Dashboard de Rareza:** Gráficos visuales que explican el ranking de cada combinación (ej. "95% original") [246, Conversación].
*   **Monitor de Aprendizaje:** Interfaz que muestra cómo la app ha ajustado su lógica tras los últimos sorteos [Conversación].
*   **Modo Dual:** Transición fluida entre generación rápida (1-click) y configuración experta.

---

## ⚙️ Metodología de Desarrollo (AI-First)
*   **Spec-Anchored:** Este documento es la fuente de verdad y evoluciona con el código [6].
*   **Plan Mode Obligatorio:** El agente debe presentar un plan detallado antes de cualquier cambio estructural y esperar aprobación humana (HITL) [7, 8].
Este arc