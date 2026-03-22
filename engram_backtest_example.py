from datetime import datetime
from engram_storage import init_db, add_memory, search_memories


def run_backtesting_session(session_id: str):
    data_points = [
        {'draw': '2026-03-20', 'predicted_score': 72.3, 'actual_win': False},
        {'draw': '2026-03-21', 'predicted_score': 85.1, 'actual_win': True},
    ]

    for i, point in enumerate(data_points, start=1):
        if point['actual_win']:
            lesson = 'El algoritmo de rareza acertó una combinación ganadora, se aumenta confianza.'
            confidence = 0.95
        else:
            lesson = 'No se acertó; recalibrar pesos de rareza para el siguiente ciclo.'
            confidence = 0.50

        add_memory(
            what=f'Backtesting ciclo {i} - {point["draw"]}',
            why='Registrar resultados de comparación de predicción vs realidad del sorteo',
            where=f'backtesting/{session_id}/engram',
            learned=lesson,
            session_id=session_id,
            confidence=confidence,
            domain='backtesting'
        )

    print('Backtesting completado para', session_id)
    print('Memorias encontradas (query: backtesting):')
    results = search_memories('backtesting')
    for r in results:
        print(f"[{r['id']}] {r['timestamp']} - {r['what']} - conf={r['confidence']}")


if __name__ == '__main__':
    init_db()
    run_backtesting_session('bt-2026-03-22')
