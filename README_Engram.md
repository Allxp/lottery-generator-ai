# Engram: Memoria Persistente Local

Sistema de memoria persistente local para el Generador Inteligente de Combinaciones de Lotería. Almacena aprendizajes en 4 dimensiones (What, Why, Where, Learned) para resolver amnesia entre sesiones.

## Inicio rápido

1. Inicializar DB:
   ```bash
   python engram_manager.py init
   ```

2. Agregar memoria desde código:
   ```python
   from engram_storage import add_memory
   add_memory("Nueva lección", "Por qué", "Dónde", "Qué aprendí")
   ```

3. Buscar memorias:
   ```bash
   python engram_manager.py search "backtesting"
   ```

4. Ver estado:
   ```bash
   python engram_manager.py status
   ```

## Integración con Cerebro Estadístico

El módulo `stats_brain.py` integra Engram en el flujo de loterías:

```python
from stats_brain import generate_ranked_combinations, run_backtesting_cycle

# Generar combinaciones con ranking
combos = generate_ranked_combinations('leidsa', 10)

# Ejecutar backtesting (registra automáticamente en Engram)
result = run_backtesting_cycle('leidsa', 'session-001')
```

### Funciones principales

- `generate_ranked_combinations(lottery, count)`: Genera combinaciones con score 1-100
- `run_backtesting_cycle(lottery, session_id)`: Compara predicciones vs resultados reales y registra aprendizaje
- `calculate_score(combination, historical_data)`: Calcula rareza basada en balance, distribución y originalidad

### Loterías soportadas

- `leidsa`: Loto Dominicano (6 números + bono + superb bono)
- `primitiva`: La Primitiva (6 números + reintegro, sin complementario)
- `euromillones`: Euromillones (5 números + 2 estrellas)
- `bonoloto`: Bonoloto (6 números)

## Job de Auto-Backtesting

Ejecuta backtesting automático diario para todas las loterías:

```bash
# Simulación (no registra en Engram)
python auto_backtest.py --dry-run

# Ejecución real
python auto_backtest.py

# Solo una lotería
python auto_backtest.py --lottery leidsa
```

### Scheduling Automático

**Windows (Task Scheduler):**
1. Crear tarea básica
2. Programar: Diario, 6:00 AM
3. Acción: Ejecutar `schedule_auto_backtest.bat`
4. Opciones: Ejecutar aunque no haya sesión iniciada

**Linux/Mac (Cron):**
```bash
# Añadir a crontab -e
0 6 * * * cd /path/to/project && python auto_backtest.py
```

### Reportes

Los reportes se generan en `reports/backtest_report_YYYYMMDD.txt` con:
- Loterías procesadas
- Precisión promedio
- Nuevos aprendizajes
- Timestamp de ejecución

## Tests

Ejecutar suite completa:
```bash
python tests/test_engram_storage.py
python tests/test_stats_brain.py
python tests/test_auto_backtest.py
```

## Integración

- Importar `engram_storage` en módulos de backtesting.
- Usar `add_memory` al finalizar tareas críticas.
- Consultar historial con `search_memories` para decisiones informadas.

## Arquitectura

- **SQLite + FTS5**: Búsqueda full-text rápida.
- **Triggers**: Sincronización automática entre tablas.
- **CLI**: Gestión sin código.
- **Tests**: Cobertura completa de operaciones CRUD + FTS.