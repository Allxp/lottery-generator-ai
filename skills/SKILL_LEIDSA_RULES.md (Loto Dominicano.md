SKILL_LEIDSA_RULES.md (Loto Dominicano)
Este módulo gestiona la complejidad de las eras históricas y la generación de la apuesta completa actual.
What: Reglas del Loto Dominicano (LEIDSA) centrado en la modalidad SuperMás
.
Why: La evolución de 6 a 8 números requiere segmentación para no sesgar las estadísticas de las nuevas tómbolas [Conversación].
Reglas de Generación:
Bloque Principal: Generar 6 números únicos (rango 1–40)
.
Bono "Más": Generar 1 número (rango 1–12)
.
SuperBono "SuperMás": Generar 1 número (rango 1–15)
.
Costo de la Jugada: Informar al usuario que la combinación completa tiene un costo de RD$200
.
Validación de Eras: Al analizar el histórico, si la fecha es anterior a la introducción del "Más" o "SuperMás", el agente debe tratar esos campos como null y no incluirlos en el promedio de frecuencia actual [Conversación].
