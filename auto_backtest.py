#!/usr/bin/env python3
"""
Auto-Backtesting Job: Ejecución automática diaria del bucle de aprendizaje

Este script se ejecuta diariamente para:
1. Verificar nuevos resultados históricos
2. Ejecutar backtesting para todas las loterías activas
3. Registrar aprendizajes en Engram
4. Generar reporte de rendimiento

Uso recomendado:
- Programar con cron/Windows Task Scheduler: diario a las 6:00 AM
- python auto_backtest.py --dry-run para simulación
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import csv

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from stats_brain import run_backtesting_cycle, generate_ranked_combinations, LOTTERY_CONFIGS
from engram_storage import add_memory, list_memories, search_memories

# Configuración
DATA_DIR = Path(__file__).parent / 'spec&data'
REPORT_DIR = Path(__file__).parent / 'reports'
REPORT_DIR.mkdir(exist_ok=True)

ACTIVE_LOTTERIES = ['leidsa', 'primitiva', 'euromillones', 'bonoloto']

def check_new_results(lottery: str) -> bool:
    """Verifica si hay resultados nuevos desde la última ejecución."""
    # Buscar en Engram la última fecha de backtesting para esta lotería
    query = f'backtesting {lottery}'
    memories = search_memories(query, limit=1)

    if not memories:
        return True  # Primera ejecución

    last_session = memories[0]['session_id']
    # Extraer fecha de session_id (formato: auto-YYYYMMDD)
    try:
        last_date_str = last_session.split('-')[1]
        last_date = datetime.strptime(last_date_str, '%Y%m%d').date()
        today = datetime.now().date()

        # Verificar si hay datos históricos más recientes que la última ejecución
        historical_dates = get_historical_dates(lottery)
        if historical_dates:
            latest_historical = max(historical_dates)
            return latest_historical > last_date

    except (ValueError, IndexError):
        pass

    return True  # Si hay duda, ejecutar

def get_historical_dates(lottery: str) -> List[datetime.date]:
    """Obtiene fechas disponibles en datos históricos."""
    files = get_lottery_files(lottery)
    dates = []

    for filepath in files:
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        date_str = row.get('Fecha', row.get('Date', ''))
                        if date_str:
                            try:
                                # Intentar diferentes formatos de fecha
                                for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y']:
                                    try:
                                        date_obj = datetime.strptime(date_str, fmt).date()
                                        dates.append(date_obj)
                                        break
                                    except ValueError:
                                        continue
                            except:
                                continue
            except Exception as e:
                print(f"Error leyendo {filepath}: {e}")

    return sorted(list(set(dates)))

def get_lottery_files(lottery: str) -> List[Path]:
    """Obtiene archivos de datos históricos para una lotería."""
    file_map = {
        'leidsa': ['historico_loto_leidsa.csv'],
        'primitiva': ['Lotoideas.com - Histórico de Resultados - Primitiva - 1985 a 2012 (1).csv',
                      'Lotoideas.com - Histórico de Resultados - Primitiva - 2013 a 202X (1).csv'],
        'euromillones': ['Lotoideas.com - Histórico de Resultados - Euromillones - 2004 a 202X.csv'],
        'bonoloto': ['Lotoideas.com - Histórico de Resultados - Bonoloto - 1988 a 2012.csv',
                     'Lotoideas.com - Histórico de Resultados - Bonoloto - 2013 a 202X.csv']
    }

    files = file_map.get(lottery, [])
    return [DATA_DIR / f for f in files]

def generate_daily_predictions(lottery: str, count: int = 20) -> List[Dict]:
    """Genera predicciones diarias con ranking."""
    return generate_ranked_combinations(lottery, count)

def run_auto_backtest(dry_run: bool = False) -> Dict:
    """Ejecuta backtesting automático para todas las loterías activas."""
    session_id = f"auto-{datetime.now().strftime('%Y%m%d')}"
    report = {
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'lotteries_processed': [],
        'total_cycles': 0,
        'total_accuracy': 0.0,
        'new_learnings': 0
    }

    print(f"🤖 Iniciando Auto-Backtesting - Sesión: {session_id}")
    print("=" * 60)

    for lottery in ACTIVE_LOTTERIES:
        print(f"\n🎯 Procesando {LOTTERY_CONFIGS[lottery]['name']}...")

        # Verificar si hay nuevos resultados
        if not check_new_results(lottery):
            print(f"   ⏭️  No hay nuevos resultados. Saltando.")
            continue

        # Generar predicciones del día
        predictions = generate_daily_predictions(lottery, 20)
        print(f"   📊 Generadas {len(predictions)} predicciones top")

        # Ejecutar backtesting
        if not dry_run:
            result = run_backtesting_cycle(lottery, session_id, predictions)
            accuracy = result['accuracy']
            print(f"   📊 Precisión: {accuracy:.1f}")
            print(f"   🧠 Aprendido: {result['learned'][:60]}...")

            report['lotteries_processed'].append(lottery)
            report['total_cycles'] += 1
            report['total_accuracy'] += accuracy
            report['new_learnings'] += 1
        else:
            print("   🔍 Dry-run: Backtesting simulado")
            report['lotteries_processed'].append(f"{lottery} (dry-run)")

    # Calcular métricas globales
    if report['total_cycles'] > 0:
        report['avg_accuracy'] = report['total_accuracy'] / report['total_cycles']
    else:
        report['avg_accuracy'] = 0.0

    # Registrar resumen en Engram
    if not dry_run and report['total_cycles'] > 0:
        summary_learned = f"Auto-backtesting completado: {report['total_cycles']} loterías procesadas, precisión promedio {report['avg_accuracy']:.1%}"
        add_memory(
            what=f'Auto-Backtesting Diario - Sesión {session_id}',
            why='Ejecución automática del bucle de aprendizaje continuo',
            where='auto_backtest.py',
            learned=summary_learned,
            session_id=session_id,
            confidence=report['avg_accuracy'],
            domain='backtesting'
        )
        print(f"\n📝 Resumen registrado en Engram: {summary_learned}")

    # Generar reporte
    generate_report(report, dry_run)

    print(f"\n✅ Auto-Backtesting completado. Procesadas: {len(report['lotteries_processed'])} loterías")
    return report

def generate_report(report: Dict, dry_run: bool):
    """Genera reporte de la sesión de backtesting."""
    report_file = REPORT_DIR / f"backtest_report_{report['session_id']}.txt"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("AUTO-BACKTESTING REPORT\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Session ID: {report['session_id']}\n")
        f.write(f"Timestamp: {report['timestamp']}\n")
        f.write(f"Loterías procesadas: {', '.join(report['lotteries_processed'])}\n")
        f.write(f"Ciclos totales: {report['total_cycles']}\n")
        f.write(f"Precisión promedio: {report['avg_accuracy']:.1%}\n")
        f.write(f"Nuevos aprendizajes: {report['new_learnings']}\n")

        if report['total_cycles'] > 0:
            f.write("\n📈 Rendimiento por lotería:\n")
            # Aquí se podría agregar detalle por lotería si se guarda

    print(f"📄 Reporte generado: {report_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Auto-Backtesting Job')
    parser.add_argument('--dry-run', action='store_true',
                       help='Simular ejecución sin registrar en Engram')
    parser.add_argument('--lottery', choices=ACTIVE_LOTTERIES,
                       help='Ejecutar solo para una lotería específica')

    args = parser.parse_args()

    if args.lottery:
        # Modo single-lottery
        session_id = f"manual-{args.lottery}-{datetime.now().strftime('%Y%m%d-%H%M')}"
        predictions = generate_daily_predictions(args.lottery, 20)
        if not args.dry_run:
            result = run_backtesting_cycle(args.lottery, session_id, predictions)
            print(f"Backtesting {args.lottery}: Precisión {result['accuracy']:.1%}")
        else:
            print(f"Dry-run: {args.lottery} - {len(predictions)} predicciones generadas")
    else:
        # Modo completo
        run_auto_backtest(args.dry_run)

if __name__ == '__main__':
    main()