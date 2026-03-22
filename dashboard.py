#!/usr/bin/env python3
"""
Dashboard Web para el Generador Inteligente de Combinaciones de Lotería

Interfaz web que permite:
- Generar combinaciones con scores
- Visualizar memoria Engram
- Ver reportes de backtesting
- Monitorear estado del sistema

Uso:
    python dashboard.py
    # Acceder en http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
from datetime import datetime
import json

# Importar módulos del sistema
from stats_brain import generate_ranked_combinations, LOTTERY_CONFIGS
from engram_storage import list_memories, search_memories
from engram_manager import cmd_status

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lottery-dashboard-key'

# Directorio del proyecto
PROJECT_DIR = Path(__file__).parent
REPORTS_DIR = PROJECT_DIR / 'reports'

@app.route('/')
def index():
    """Página principal del dashboard."""
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Página de generación de combinaciones."""
    if request.method == 'POST':
        lottery = request.form.get('lottery', 'leidsa')
        count = int(request.form.get('count', 5))

        try:
            combinations = generate_ranked_combinations(lottery, count)
            return render_template('generate.html',
                                 combinations=combinations,
                                 lottery=lottery,
                                 lottery_name=LOTTERY_CONFIGS[lottery]['name'])
        except Exception as e:
            return render_template('generate.html', error=str(e))

    return render_template('generate.html')

@app.route('/memory')
def memory():
    """Página de visualización de memoria Engram."""
    try:
        # Obtener parámetros de filtro
        domain = request.args.get('domain', '')
        limit = int(request.args.get('limit', 50))

        if domain:
            # Buscar por dominio
            memories = search_memories(f'domain:{domain}', limit=limit)
        else:
            memories = list_memories(limit=limit)

        # Estadísticas
        total_memories = len(memories)
        domains = {}
        for m in memories:
            d = m.get('domain', 'unknown')
            domains[d] = domains.get(d, 0) + 1

        return render_template('memory.html',
                             memories=memories,
                             total_memories=total_memories,
                             domains=domains,
                             current_domain=domain)

    except Exception as e:
        return render_template('memory.html', error=str(e))

@app.route('/reports')
def reports():
    """Página de reportes de backtesting."""
    try:
        # Calcular métricas del sistema
        total_backtests = 0
        backtests_today = 0
        avg_accuracy = 0.0
        accuracy_change = 0.0
        total_predictions = 0
        predictions_today = 0
        active_games = len(LOTTERY_CONFIGS)

        # Obtener datos de backtesting desde Engram
        backtest_memories = search_memories('backtesting', limit=1000)

        if backtest_memories:
            total_backtests = len(backtest_memories)

            # Calcular backtests de hoy
            today = datetime.now().date()
            for memory in backtest_memories:
                if memory.get('timestamp', '').startswith(str(today)):
                    backtests_today += 1

            # Calcular precisión promedio (simulado por ahora)
            accuracies = []
            for memory in backtest_memories[-50:]:  # Últimos 50
                learned = memory.get('learned', '')
                if '%' in learned:
                    try:
                        acc = float(learned.split('%')[0].split()[-1])
                        accuracies.append(acc)
                    except:
                        pass

            if accuracies:
                avg_accuracy = sum(accuracies) / len(accuracies)
                accuracy_change = accuracies[-1] - accuracies[0] if len(accuracies) > 1 else 0.0
            else:
                avg_accuracy = 0.0
                accuracy_change = 0.0

        # Obtener predicciones generadas
        prediction_memories = search_memories('prediction', limit=1000)
        total_predictions = len(prediction_memories)

        today = datetime.now().date()
        for memory in prediction_memories:
            if memory.get('timestamp', '').startswith(str(today)):
                predictions_today += 1

        # Estado del sistema
        system_uptime = "24h 30m"  # Simulado
        memory_usage = 45  # Simulado
        db_size = "2.3 MB"  # Simulado
        last_backup = "2024-01-15 14:30"  # Simulado
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Rendimiento por juego
        game_performance = []
        for game_id, config in LOTTERY_CONFIGS.items():
            # Buscar memorias relacionadas con este juego
            game_memories = search_memories(game_id, limit=100)
            last_backtest = "Nunca"
            accuracy = 0.0
            predictions_today_game = 0

            if game_memories:
                # Encontrar último backtest
                for memory in game_memories:
                    what = memory.get('what', '').lower()
                    if 'backtest' in what or 'predic' in what:
                        last_backtest = memory.get('timestamp', '')[:19]
                        break

                # Calcular precisión
                accuracies = []
                for memory in game_memories:
                    learned = memory.get('learned', '')
                    if '%' in learned:
                        try:
                            acc = float(learned.split('%')[0].split()[-1])
                            accuracies.append(acc)
                        except:
                            pass
                if accuracies:
                    accuracy = sum(accuracies) / len(accuracies)

            # Predicciones de hoy para este juego
            for memory in prediction_memories:
                if memory.get('timestamp', '').startswith(str(today)) and game_id in memory.get('where', ''):
                    predictions_today_game += 1

            # Determinar estado
            if game_memories and last_backtest != "Nunca":
                status = "good"
                status_display = "Activo"
            elif game_memories:
                status = "warning"
                status_display = "Sin backtest reciente"
            else:
                status = "error"
                status_display = "Inactivo"

            game_performance.append({
                'id': game_id,
                'name': config['name'],
                'status': status,
                'status_display': status_display,
                'last_backtest': last_backtest,
                'accuracy': accuracy,
                'predictions_today': predictions_today_game
            })

        # Alertas del sistema (simuladas)
        alerts = []
        if backtests_today == 0:
            alerts.append({
                'level': 'warning',
                'message': 'No se han ejecutado backtests hoy',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        if avg_accuracy < 30:
            alerts.append({
                'level': 'error',
                'message': 'Precisión promedio por debajo del 30%',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return render_template('reports.html',
                             total_backtests=total_backtests,
                             backtests_today=backtests_today,
                             avg_accuracy=round(avg_accuracy, 1),
                             accuracy_change=round(accuracy_change, 1),
                             total_predictions=total_predictions,
                             predictions_today=predictions_today,
                             active_games=active_games,
                             system_uptime=system_uptime,
                             memory_usage=memory_usage,
                             db_size=db_size,
                             last_backup=last_backup,
                             last_update=last_update,
                             game_performance=game_performance,
                             alerts=alerts)

    except Exception as e:
        return render_template('reports.html', error=str(e))

@app.route('/api/status')
def api_status():
    """API endpoint para estado del sistema."""
    try:
        # Obtener datos directamente desde engram_storage
        total_memories = len(list_memories(1000))
        all_memories = list_memories(1000)

        # Calcular estadísticas de dominios
        domains = {}
        for m in all_memories:
            d = m.get('domain', 'unknown')
            domains[d] = domains.get(d, 0) + 1

        return jsonify({
            'total_memories': total_memories,
            'domains': domains,
            'timestamp': datetime.now().isoformat(),
            'status': 'operational'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reports/<game_id>/details')
def game_details(game_id):
    """Detalles de rendimiento de un juego específico."""
    try:
        if game_id not in LOTTERY_CONFIGS:
            return render_template('reports.html', error=f"Juego {game_id} no encontrado")

        config = LOTTERY_CONFIGS[game_id]
        game_memories = search_memories(f'game:{game_id}', limit=200)

        # Calcular estadísticas
        total_backtests = len([m for m in game_memories if 'backtest' in m.get('what', '').lower()])
        total_predictions = len([m for m in game_memories if 'prediction' in m.get('what', '').lower()])

        # Últimos 10 backtests
        backtests = [m for m in game_memories if 'backtest' in m.get('what', '').lower()][:10]

        return render_template('game_details.html',
                             game_id=game_id,
                             game_name=config['name'],
                             total_backtests=total_backtests,
                             total_predictions=total_predictions,
                             backtests=backtests)

    except Exception as e:
        return render_template('reports.html', error=str(e))

@app.route('/reports/run-all-backtests')
def run_all_backtests():
    """Ejecutar backtests para todos los juegos."""
    try:
        from stats_brain import run_backtesting_cycle

        # Ejecutar backtesting para todos los juegos
        results = {}
        for game_id in LOTTERY_CONFIGS.keys():
            try:
                result = run_backtesting_cycle(game_id)
                results[game_id] = {'success': True, 'result': result}
            except Exception as e:
                results[game_id] = {'success': False, 'error': str(e)}

        success_count = sum(1 for r in results.values() if r['success'])

        return render_template('reports.html',
                             success=f"Se ejecutaron backtests exitosamente para {success_count}/{len(LOTTERY_CONFIGS)} juegos")

    except Exception as e:
        return render_template('reports.html', error=str(e))

@app.route('/reports/clean-old-data')
def clean_old_data():
    """Limpiar datos antiguos de la base de datos."""
    try:
        from engram_storage import clean_old_memories

        # Limpiar memorias antiguas (más de 90 días)
        deleted_count = clean_old_memories(days=90)

        return render_template('reports.html',
                             success=f"Se limpiaron {deleted_count} memorias antiguas")

    except Exception as e:
        return render_template('reports.html', error=str(e))

@app.route('/reports/backup-database')
def backup_database():
    """Crear backup de la base de datos."""
    try:
        from engram_manager import cmd_backup
        import io
        import sys
        from contextlib import redirect_stdout

        # Ejecutar backup
        f = io.StringIO()
        with redirect_stdout(f):
            cmd_backup(type('Args', (), {'output': None})())
        backup_output = f.getvalue()

        return render_template('reports.html',
                             success="Backup de la base de datos creado exitosamente")

    except Exception as e:
        return render_template('reports.html', error=str(e))

@app.route('/reports/<game_id>/run-backtest')
def run_game_backtest(game_id):
    """Ejecutar backtest para un juego específico."""
    try:
        if game_id not in LOTTERY_CONFIGS:
            return render_template('reports.html', error=f"Juego {game_id} no encontrado")

        from stats_brain import run_backtesting_cycle

        # Ejecutar backtesting para el juego específico
        result = run_backtesting_cycle(game_id)

        return render_template('reports.html',
                             success=f"Backtest completado para {LOTTERY_CONFIGS[game_id]['name']}. Resultado: {result}")

    except Exception as e:
        return render_template('reports.html', error=str(e))

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    templates_dir = PROJECT_DIR / 'templates'
    templates_dir.mkdir(exist_ok=True)

    print("🚀 Iniciando Dashboard del Generador de Lotería...")
    print("📱 Acceder en: http://localhost:5000")
    print("❌ Presiona Ctrl+C para detener")

    app.run(debug=True, host='0.0.0.0', port=5000)