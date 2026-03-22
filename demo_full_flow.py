#!/usr/bin/env python3
"""
Ejemplo completo: Generador Inteligente de Combinaciones de Lotería con Engram

Este script demuestra el flujo completo:
1. Generación de combinaciones con ranking inteligente
2. Backtesting contra datos históricos
3. Registro de aprendizajes en Engram
4. Consulta de memoria acumulada
"""

from stats_brain import generate_ranked_combinations, run_backtesting_cycle
from engram_storage import list_memories, search_memories
from engram_manager import cmd_status
import argparse

def demo_full_flow(lottery: str = 'leidsa', session_id: str = None):
    """Demuestra el flujo completo de generación + backtesting + memoria."""
    print(f"🚀 Iniciando demo para {lottery.upper()}")
    print("=" * 50)

    # 1. Generar combinaciones top
    print("🎯 Generando combinaciones con ranking inteligente...")
    top_combos = generate_ranked_combinations(lottery, 5)

    print("Top 5 combinaciones:")
    for i, combo in enumerate(top_combos, 1):
        main = combo['main_numbers']
        score = combo['score']
        extra = ""
        if lottery == 'leidsa':
            extra = f" + {combo.get('bonus', '?')} + {combo.get('super_bonus', '?')}"
        elif lottery == 'primitiva':
            extra = f" + R:{combo.get('reintegro', '?')}"
        elif lottery == 'euromillones':
            extra = f" + ⭐ {combo.get('stars', [])}"

        winner_tag = " 🏆 GANADORA PREVIA" if 'historical_winner' in combo else ""
        print(f"{i}. Score {score}: {main}{extra}{winner_tag}")

    print("\n" + "=" * 50)

    # 2. Ejecutar backtesting
    print("🔄 Ejecutando backtesting contra datos históricos...")
    if not session_id:
        from datetime import datetime
        session_id = f"demo-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    result = run_backtesting_cycle(lottery, session_id, top_combos)

    print(f"📊 Resultados del backtesting:")
    print(f"   - Predicciones analizadas: {result['predictions_count']}")
    print(f"   - Aciertos en top ranking: {result['matches']}")
    print(f"   - Precisión: {result['accuracy']:.1%}")
    print(f"   - Sesión: {result['session_id']}")
    print(f"   - Aprendido: {result['learned']}")

    print("\n" + "=" * 50)

    # 3. Consultar memoria acumulada
    print("🧠 Memoria Engram actualizada:")
    memories = list_memories(10)
    backtesting_memories = [m for m in memories if m['domain'] == 'backtesting']

    print(f"Total memorias de backtesting: {len(backtesting_memories)}")
    print("\nÚltimas 3 lecciones aprendidas:")
    for memory in backtesting_memories[-3:]:
        print(f"• [{memory['timestamp'][:19]}] {memory['what']}")
        print(f"  Confianza: {memory['confidence']:.1f}")
        print(f"  Lección: {memory['learned'][:80]}...")
        print()

    print("✅ Demo completada. El sistema ha aprendido de este ciclo.")

def main():
    parser = argparse.ArgumentParser(description='Demo completo del Generador de Lotería con Engram')
    parser.add_argument('--lottery', choices=['leidsa', 'primitiva', 'euromillones', 'bonoloto'],
                       default='leidsa', help='Lotería a usar (default: leidsa)')
    parser.add_argument('--session', help='ID de sesión personalizado')

    args = parser.parse_args()
    demo_full_flow(args.lottery, args.session)

if __name__ == '__main__':
    main()