# Engram Registry (Memoria Persistente)

## Propósito
Registrar el esquema y el comportamiento del almacenamiento local Engram para rastrear aprendizajes críticos y asegurar trazabilidad de decisiones por sesión.

## Ruta
- `/data/engram.db` (SQLite + FTS5)

## Tablas
- `cognitive_stack`
  - id (INTEGER PK AUTOINCREMENT)
  - timestamp (DATETIME DEFAULT CURRENT_TIMESTAMP)
  - what (TEXT, no nulo)
  - why (TEXT, no nulo)
  - where (TEXT, no nulo)
  - learned (TEXT, no nulo)
  - session_id (TEXT opcional)
  - confidence (REAL DEFAULT 1.0)
  - domain (TEXT opcional)

- `cognitive_stack_fts` (virtual, FTS5)
  - what
  - why
  - learned
  - contenido: `cognitive_stack`

## Archivos relacionados
- `engram_storage.py`: API de persistencia (init, add, list, search)
- `engram_manager.py`: CLI para gestión (init, status, backup, search)
- `engram_backtest_example.py`: Ejemplo de integración con backtesting
- `stats_brain.py`: Cerebro estadístico con integración Engram
- `auto_backtest.py`: Job automático de backtesting diario
- `schedule_auto_backtest.bat`: Script de scheduling para Windows
- `tests/test_engram_storage.py`: Suite de tests unitarios para Engram
- `tests/test_stats_brain.py`: Tests para cerebro estadístico
- `tests/test_auto_backtest.py`: Tests para job automático
- `memories/repo/engram-registry.md`: Este archivo

## Reglas de uso
1. Cada tarea compleja debe tener al menos un registro en esta tabla.
2. Evitar texto sensitivo (no guardar datos privados ni secrets).
3. No depender de la inserción directa sin API; usar `engram_storage` o `engram_manager`.
4. Consultar antes de limpiar historiales; los borrados deben ser explícitos y auditados.

## Convención de dominios
- `architecture`, `stats`, `data_pipeline`, `ui`, `backtesting`, `rules`.

## Backups
- Copia diaria recomendada (externa manual/local), preferible antes de migraciones estructurales.
- Comando: `python engram_manager.py backup`
