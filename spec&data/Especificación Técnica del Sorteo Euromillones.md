📘 Especificación Técnica del Sorteo Euromillones
(Versión para uso en desarrollo de aplicaciones)
🎯 Objetivo del Juego
Euromillones es un sorteo europeo en el que el jugador debe seleccionar una combinación formada por:
- 5 números del 1 al 50
- 2 estrellas del 1 al 12
Cada combinación válida constituye una apuesta.

🧩 Estructura de la Apuesta
Apuesta Sencilla
- Selección de 5 números únicos entre 1–50
- Selección de 2 estrellas únicas entre 1–12
- Precio por apuesta: 2,50 €
Apuestas Múltiples
El jugador puede seleccionar:
- Más de 5 números (hasta 10)
- Más de 2 estrellas (hasta 5)
Esto genera múltiples combinaciones automáticas.
El precio final depende del número total de combinaciones generadas.
Límite por boleto
- Hasta 5 apuestas sencillas por boleto
(o una apuesta múltiple equivalente)

📅 Frecuencia de Sorteos
- Dos sorteos por semana:
- Martes
- Viernes
El usuario puede elegir:
- Participar solo en el siguiente sorteo
- Participar en ambos sorteos de la semana
- Repetir la misma compra durante varias semanas (suscripción)

🛒 Flujo de Participación (para UI/UX o backend)
- Elegir sorteo(s)
- Próximo sorteo
- Ambos sorteos de la semana
- Repetición semanal opcional
- Seleccionar combinación(es)
- Manualmente
- Generación automática (aleatoria)
- Configurar número de apuestas
- Hasta 5 sencillas
- O una apuesta múltiple
- Añadir al carrito / compra
- Confirmar compra
- Revisar combinaciones
- Revisar sorteos seleccionados
- Confirmar o editar
- Finalizar y registrar la participación

💰 Distribución de Premios
- 50% de la recaudación total se destina a premios.
- Existen múltiples categorías de premio según aciertos (5+2, 5+1, 5+0, 4+2, etc.).
- El bote puede acumularse si no hay acertantes de primera categoría.
(Si quieres, puedo generarte también la tabla completa de categorías y probabilidades.)

🔒 Validaciones para Backend
Validación de apuesta sencilla
- numbers.length === 5
- stars.length === 2
- Todos los números deben ser únicos
- Rango válido:
- 1 ≤ number ≤ 50
- 1 ≤ star ≤ 12
Validación de apuesta múltiple
- numbers.length >= 5 && numbers.length <= 10
- stars.length >= 2 && stars.length <= 5
- Cálculo de combinaciones:
- C(numbers, 5) * C(stars, 2)
Validación de compra
- Máximo 5 apuestas sencillas por boleto
- O una única apuesta múltiple
- Precio total = combinaciones * 2,50 €
