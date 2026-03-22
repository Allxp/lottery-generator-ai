import random
import csv
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from engram_storage import add_memory

# Configuración por lotería
LOTTERY_CONFIGS = {
    'leidsa': {
        'main_range': (1, 40),
        'main_count': 6,
        'bonus_range': (1, 12),
        'super_bonus_range': (1, 15),
        'name': 'Loto Dominicano (LEIDSA)',
        'cost': 'RD$200'
    },
    'primitiva': {
        'main_range': (1, 49),
        'main_count': 6,
        'reintegro_range': (0, 9),
        'name': 'La Primitiva',
        'no_complementario': True  # No generar complementario
    },
    'euromillones': {
        'main_range': (1, 50),
        'main_count': 5,
        'stars_range': (1, 12),
        'stars_count': 2,
        'name': 'Euromillones'
    },
    'bonoloto': {
        'main_range': (1, 49),
        'main_count': 6,
        'name': 'Bonoloto'
    }
}

def generate_combination(lottery: str) -> Dict:
    """Genera una combinación aleatoria para la lotería especificada."""
    config = LOTTERY_CONFIGS[lottery]

    # Generar números principales únicos
    main_numbers = sorted(random.sample(range(config['main_range'][0], config['main_range'][1] + 1), config['main_count']))

    result = {
        'lottery': lottery,
        'main_numbers': main_numbers,
        'timestamp': datetime.now().isoformat()
    }

    # Agregar elementos específicos por lotería
    if lottery == 'leidsa':
        result['bonus'] = random.randint(config['bonus_range'][0], config['bonus_range'][1])
        result['super_bonus'] = random.randint(config['super_bonus_range'][0], config['super_bonus_range'][1])
        result['cost'] = config['cost']
    elif lottery == 'primitiva':
        result['reintegro'] = random.randint(config['reintegro_range'][0], config['reintegro_range'][1])
    elif lottery == 'euromillones':
        result['stars'] = sorted(random.sample(range(config['stars_range'][0], config['stars_range'][1] + 1), config['stars_count']))

    return result

def calculate_score(combination: Dict, historical_data: List[Dict] = None) -> Tuple[Dict, float]:
    """Calcula el score de rareza para una combinación (1-100)."""
    score = 50.0  # Base neutral

    main_numbers = combination['main_numbers']

    # Balance par/impar
    even_count = sum(1 for n in main_numbers if n % 2 == 0)
    odd_count = len(main_numbers) - even_count
    balance_penalty = abs(even_count - odd_count) * 5
    score -= balance_penalty

    # Distribución de rango
    low_count = sum(1 for n in main_numbers if n <= len(main_numbers) * 2)
    high_count = len(main_numbers) - low_count
    range_penalty = abs(low_count - high_count) * 3
    score -= range_penalty

    # Anti-patrones: secuencias aritméticas
    diffs = [main_numbers[i+1] - main_numbers[i] for i in range(len(main_numbers)-1)]
    if len(set(diffs)) == 1:  # Secuencia aritmética
        score -= 20

    # Originalidad histórica
    if historical_data:
        for hist in historical_data:
            if hist.get('main_numbers') == main_numbers:
                combination['historical_winner'] = hist.get('date', 'Unknown')
                score += 10  # Bonus por ser ganadora previa (no penalización)

    # Clamp score
    score = max(1, min(100, score))

    combination['score'] = round(score, 1)
    combination['score_explanation'] = f"Balance P/I: {even_count}/{odd_count}, Rango: {low_count}/{high_count}"

    return combination, score

def load_historical_data(lottery: str) -> List[Dict]:
    """Carga datos históricos desde CSV."""
    data_dir = os.path.join(os.getcwd(), 'spec&data')
    files = {
        'leidsa': 'historico_loto_leidsa.csv',
        'primitiva': ['Lotoideas.com - Histórico de Resultados - Primitiva - 1985 a 2012 (1).csv',
                      'Lotoideas.com - Histórico de Resultados - Primitiva - 2013 a 202X (1).csv'],
        'euromillones': 'Lotoideas.com - Histórico de Resultados - Euromillones - 2004 a 202X.csv',
        'bonoloto': ['Lotoideas.com - Histórico de Resultados - Bonoloto - 1988 a 2012.csv',
                     'Lotoideas.com - Histórico de Resultados - Bonoloto - 2013 a 202X.csv']
    }

    historical = []
    file_list = files.get(lottery, [])
    if isinstance(file_list, str):
        file_list = [file_list]

    for filename in file_list:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Adaptar formato según lotería
                        hist_entry = {'date': row.get('Fecha', row.get('Date', ''))}
                        if lottery == 'leidsa':
                            # Parsear números de LEIDSA
                            numbers = []
                            for i in range(1, 7):  # Números principales
                                num = row.get(f'Bola{i}')
                                if num and num.isdigit():
                                    numbers.append(int(num))
                            hist_entry['main_numbers'] = sorted(numbers) if numbers else []
                        elif lottery in ['primitiva', 'bonoloto']:
                            numbers = []
                            for col in ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']:
                                num = row.get(col)
                                if num and num.isdigit():
                                    numbers.append(int(num))
                            hist_entry['main_numbers'] = sorted(numbers) if numbers else []
                        elif lottery == 'euromillones':
                            numbers = []
                            stars = []
                            for i in range(1, 6):
                                num = row.get(f'N{i}')
                                if num and num.isdigit():
                                    numbers.append(int(num))
                            for i in range(1, 3):
                                star = row.get(f'E{i}')
                                if star and star.isdigit():
                                    stars.append(int(star))
                            hist_entry['main_numbers'] = sorted(numbers) if numbers else []
                            hist_entry['stars'] = sorted(stars) if stars else []
                        historical.append(hist_entry)
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    return historical

def run_backtesting_cycle(lottery: str, session_id: str, top_predictions: List[Dict] = None) -> Dict:
    """Ejecuta un ciclo de backtesting y registra aprendizaje en Engram."""
    if top_predictions is None:
        # Generar predicciones de ejemplo
        top_predictions = []
        historical = load_historical_data(lottery)
        for _ in range(20):
            combo = generate_combination(lottery)
            calculate_score(combo, historical)
            top_predictions.append(combo)

    # Simular resultado real (último histórico o aleatorio)
    historical = load_historical_data(lottery)
    if historical:
        actual_result = historical[-1]  # Último resultado real
    else:
        actual_result = generate_combination(lottery)

    # Comparar predicciones con resultado real
    matches = []
    for pred in top_predictions:
        if pred['main_numbers'] == actual_result.get('main_numbers', []):
            matches.append(pred)

    # Calcular precisión
    accuracy = len(matches) / len(top_predictions) if top_predictions else 0

    # Registrar en Engram
    if accuracy > 0:
        learned = f"El sistema acertó {len(matches)} de {len(top_predictions)} predicciones top. Precisión: {accuracy:.2%}"
        confidence = min(1.0, accuracy * 2)  # Escalado
    else:
        learned = f"No se acertaron predicciones top. Necesaria recalibración de pesos de rareza."
        confidence = 0.3

    add_memory(
        what=f'Backtesting {LOTTERY_CONFIGS[lottery]["name"]} - Ciclo {session_id}',
        why='Evaluar precisión del algoritmo de ranking contra resultados reales históricos',
        where=f'stats_brain/backtesting/{lottery}',
        learned=learned,
        session_id=session_id,
        confidence=confidence,
        domain='backtesting'
    )

    return {
        'lottery': lottery,
        'session_id': session_id,
        'predictions_count': len(top_predictions),
        'matches': len(matches),
        'accuracy': accuracy,
        'actual_result': actual_result,
        'learned': learned
    }

def generate_ranked_combinations(lottery: str, count: int = 10) -> List[Dict]:
    """Genera combinaciones con ranking inteligente."""
    historical = load_historical_data(lottery)
    combinations = []

    for _ in range(count * 2):  # Generar más para seleccionar top
        combo = generate_combination(lottery)
        calculate_score(combo, historical)
        combinations.append(combo)

    # Ordenar por score descendente
    combinations.sort(key=lambda x: x['score'], reverse=True)
    return combinations[:count]

if __name__ == '__main__':
    # Ejemplo de uso
    print("Generando combinaciones LEIDSA con ranking...")
    combos = generate_ranked_combinations('leidsa', 5)
    for combo in combos:
        print(f"Score {combo['score']}: {combo['main_numbers']} + {combo.get('bonus', 'N/A')} + {combo.get('super_bonus', 'N/A')}")

    print("\nEjecutando backtesting...")
    result = run_backtesting_cycle('leidsa', 'demo-2026-03-22')
    print(f"Precisión: {result['accuracy']:.2%}")
    print(f"Aprendido: {result['learned']}")