 Especificación Técnica del Sorteo Loto Dominicano (LEIDSA)
🧩 Modalidades Disponibles
LEIDSA ofrece tres juegos relacionados, todos basados en la misma matriz principal (6 números del 1 al 40), pero con variaciones mediante bolas adicionales.
Las modalidades son:
- Loto
- Más
- SuperMás
Los sorteos se realizan miércoles y sábados a las 8:55 PM.

🎯 1. LOTO (Juego Base)
✔️ Selección
- Elegir 6 números del 1 al 40.
✔️ Precio
- RD$50 por jugada.
✔️ Cómo se gana
Hay 4 categorías de premios:
- 6 aciertos → Premio mayor (mínimo RD$20 millones).
- 5 aciertos.
- 4 aciertos.
- 3 aciertos.
✔️ Reglas para la app
- Cada combinación es un arreglo de 6 enteros únicos entre 1 y 40.
- No se permiten números repetidos.
- Orden no importa (combinación, no permutación).
✔️ Ejemplo de estructura JSON
{
  "game": "Loto",
  "numbers": [3, 12, 18, 25, 33, 40]
}



🎯 2. MÁS (Loto + Bono)
✔️ Selección
- Elegir 6 números del 1 al 40 (igual que Loto).
- Elegir 1 número Bono del 1 al 12.
✔️ Precio
- RD$50 adicionales sobre la jugada base.
- Total por jugada Loto + Más = RD$100.
✔️ Cómo se gana
- Aciertos desde 4 números + Bono hasta 6 + Bono.
- Premio mayor garantizado: mínimo RD$150 millones.
✔️ Reglas para la app
- La combinación incluye:
- 6 números únicos (1–40)
- 1 número bono (1–12)
✔️ Ejemplo JSON
{
  "game": "Mas",
  "numbers": [4, 11, 19, 22, 31, 37],
  "bonus": 7
}



🎯 3. SUPERMÁS (Loto + Bono + SuperBono)
✔️ Selección
- Elegir 6 números del 1 al 40.
- Elegir 1 Bono del 1 al 12.
- Elegir 1 SuperBono del 1 al 15.
✔️ Precio
- RD$100 adicionales sobre Loto + Más.
- Total por jugada Loto + Más + SuperMás = RD$200.
✔️ Cómo se gana
- Puedes ganar desde acertar Bono + SuperBono.
- Premio mayor: 6 números + SuperBono → RD$250 millones.
- Si aciertas 6 + Bono + SuperBono, puedes superar los RD$420 millones.
✔️ Reglas para la app
- La combinación incluye:
- 6 números únicos (1–40)
- 1 Bono (1–12)
- 1 SuperBono (1–15)
✔️ Ejemplo JSON
{
  "game": "SuperMas",
  "numbers": [2, 9, 14, 20, 33, 38],
  "bonus": 4,
  "superbonus": 11
}



🧮 Reglas Comunes para Generación de Combinaciones
✔️ Validaciones
- Los 6 números deben ser únicos.
- Rango válido:
- Loto: 1–40
- Bono: 1–12
- SuperBono: 1–15
- Orden no importa.
✔️ Formatos recomendados
- Array ordenado ascendente para consistencia.
- Identificador de modalidad obligatorio.

🛠️ Estructura Recomendada para spec.md
Puedo generarte el archivo completo si quieres, pero aquí tienes el esquema:
# Loto Dominicano (LEIDSA) – Especificación Técnica

## Modalidades
- Loto
- Más
- SuperMás

## Reglas de selección
### Loto
- 6 números (1–40)
- Precio: RD$50

### Más
- 6 números (1–40)
- 1 Bono (1–12)
- Precio adicional: RD$50

### SuperMás
- 6 números (1–40)
- 1 Bono (1–12)
- 1 SuperBono (1–15)
- Precio adicional: RD$100

## Validaciones
- Números únicos
- Rangos correctos
- Orden no relevante

## Estructuras JSON
- Ejemplos para cada modalidad

## Sorteos
- Miércoles y sábados – 8:55 PM




