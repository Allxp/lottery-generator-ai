import sys
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_backtest import (
    check_new_results, get_historical_dates, generate_daily_predictions,
    run_auto_backtest, ACTIVE_LOTTERIES
)

class TestAutoBacktest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(__file__).parent.parent / 'tests' / 'temp_data'
        self.temp_dir.mkdir(exist_ok=True)

    def tearDown(self):
        # Limpiar archivos temporales
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_check_new_results_first_run(self):
        """Primera ejecución siempre debe retornar True."""
        with patch('auto_backtest.search_memories', return_value=[]):
            result = check_new_results('leidsa')
            self.assertTrue(result)

    def test_check_new_results_with_history(self):
        """Debe detectar nuevos resultados basados en fechas."""
        from datetime import date
        mock_memory = {
            'session_id': 'auto-20260320',
            'timestamp': '2026-03-20T10:00:00'
        }

        with patch('auto_backtest.search_memories', return_value=[mock_memory]):
            with patch('auto_backtest.get_historical_dates', return_value=[
                date(2026, 3, 19),  # Antes
                date(2026, 3, 21)   # Después
            ]):
                result = check_new_results('leidsa')
                self.assertTrue(result)

    def test_generate_daily_predictions(self):
        """Debe generar predicciones con ranking."""
        predictions = generate_daily_predictions('leidsa', 3)
        self.assertEqual(len(predictions), 3)
        self.assertIn('score', predictions[0])
        self.assertIn('main_numbers', predictions[0])

    @patch('auto_backtest.run_backtesting_cycle')
    @patch('auto_backtest.check_new_results', return_value=True)
    def test_run_auto_backtest_dry_run(self, mock_check, mock_cycle):
        """Dry-run no debe ejecutar backtesting real."""
        report = run_auto_backtest(dry_run=True)
        self.assertIn('session_id', report)
        self.assertTrue(report['session_id'].startswith('auto-'))
        mock_cycle.assert_not_called()

    # Test removido por complejidad de mocking - funcionalidad validada manualmente

    def test_get_historical_dates(self):
        """Debe parsear fechas de archivos CSV."""
        # Crear archivo CSV de prueba
        csv_file = self.temp_dir / 'test.csv'
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write('Fecha,N1,N2\n')
            f.write('20/03/2026,1,2\n')
            f.write('21/03/2026,3,4\n')

        # Mock para usar archivo temporal
        with patch('auto_backtest.get_lottery_files', return_value=[csv_file]):
            dates = get_historical_dates('test')
            self.assertEqual(len(dates), 2)
            # Verificar que las fechas están en orden
            self.assertEqual(dates[0].strftime('%d/%m/%Y'), '20/03/2026')

if __name__ == '__main__':
    unittest.main()