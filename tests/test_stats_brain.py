import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import unittest
from stats_brain import (
    generate_combination, calculate_score, load_historical_data,
    run_backtesting_cycle, generate_ranked_combinations, LOTTERY_CONFIGS
)

class TestStatsBrain(unittest.TestCase):
    def test_generate_combination_leidsa(self):
        combo = generate_combination('leidsa')
        self.assertEqual(len(combo['main_numbers']), 6)
        self.assertIn('bonus', combo)
        self.assertIn('super_bonus', combo)
        self.assertEqual(combo['lottery'], 'leidsa')

    def test_generate_combination_primitiva(self):
        combo = generate_combination('primitiva')
        self.assertEqual(len(combo['main_numbers']), 6)
        self.assertIn('reintegro', combo)
        self.assertEqual(combo['lottery'], 'primitiva')

    def test_calculate_score_basic(self):
        combo = {
            'main_numbers': [1, 2, 3, 4, 5, 6],  # Mala distribución
            'lottery': 'leidsa'
        }
        result, score = calculate_score(combo)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 1)
        self.assertLessEqual(score, 100)
        self.assertIn('score', result)

    def test_load_historical_data_leidsa(self):
        data = load_historical_data('leidsa')
        self.assertIsInstance(data, list)
        if data:
            self.assertIn('main_numbers', data[0])

    def test_generate_ranked_combinations(self):
        combos = generate_ranked_combinations('leidsa', 3)
        self.assertEqual(len(combos), 3)
        # Verificar que están ordenados por score descendente
        scores = [c['score'] for c in combos]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_run_backtesting_cycle(self):
        result = run_backtesting_cycle('leidsa', 'test-session-001')
        self.assertIn('accuracy', result)
        self.assertIn('predictions_count', result)
        self.assertIn('matches', result)
        self.assertIsInstance(result['accuracy'], float)
        self.assertGreaterEqual(result['accuracy'], 0)
        self.assertLessEqual(result['accuracy'], 1)

if __name__ == '__main__':
    unittest.main()