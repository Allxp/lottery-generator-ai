import os
import sqlite3
from typing import List, Dict, Optional

ENGRAM_DB_PATH = os.path.join(os.getcwd(), 'data', 'engram.db')

CREATE_COGNITIVE_STACK_SQL = '''
CREATE TABLE IF NOT EXISTS cognitive_stack (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    what TEXT NOT NULL,
    why TEXT NOT NULL,
    "where" TEXT NOT NULL,
    learned TEXT NOT NULL,
    session_id TEXT,
    confidence REAL DEFAULT 1.0,
    domain TEXT
);
'''

CREATE_COGNITIVE_STACK_FTS_SQL = '''
CREATE VIRTUAL TABLE IF NOT EXISTS cognitive_stack_fts USING fts5(
    what, why, learned,
    content="cognitive_stack", content_rowid="id"
);
'''

CREATE_COGNITIVE_STACK_FTS_TRIGGERS = '''
CREATE TRIGGER IF NOT EXISTS cognitive_stack_ai AFTER INSERT ON cognitive_stack BEGIN
  INSERT INTO cognitive_stack_fts(rowid, what, why, learned)
  VALUES (new.id, new.what, new.why, new.learned);
END;

CREATE TRIGGER IF NOT EXISTS cognitive_stack_ad AFTER DELETE ON cognitive_stack BEGIN
  DELETE FROM cognitive_stack_fts WHERE rowid = old.id;
END;

CREATE TRIGGER IF NOT EXISTS cognitive_stack_au AFTER UPDATE ON cognitive_stack BEGIN
  UPDATE cognitive_stack_fts
  SET what = new.what, why = new.why, learned = new.learned
  WHERE rowid = old.id;
END;
'''

INSERT_MEMORY_SQL = '''
INSERT INTO cognitive_stack (what, why, "where", learned, session_id, confidence, domain)
VALUES (?, ?, ?, ?, ?, ?, ?);
'''


SEARCH_FTS_SQL = '''
SELECT cs.id, cs.timestamp, cs.what, cs.why, cs."where", cs.learned, cs.session_id, cs.confidence, cs.domain
FROM cognitive_stack cs
JOIN cognitive_stack_fts fts ON fts.rowid = cs.id
WHERE cognitive_stack_fts MATCH ?
ORDER BY cs.timestamp DESC
LIMIT ?;
'''

SELECT_ALL_SQL = '''
SELECT id, timestamp, what, why, "where", learned, session_id, confidence, domain
FROM cognitive_stack
ORDER BY timestamp DESC
LIMIT ?;
'''


def init_db(db_path: Optional[str] = None) -> str:
    db_path = db_path or ENGRAM_DB_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute(CREATE_COGNITIVE_STACK_SQL)
    conn.execute(CREATE_COGNITIVE_STACK_FTS_SQL)
    conn.executescript(CREATE_COGNITIVE_STACK_FTS_TRIGGERS)
    conn.commit()
    conn.close()
    return db_path


def add_memory(what: str, why: str, where: str, learned: str,
               session_id: Optional[str] = None, confidence: float = 1.0,
               domain: Optional[str] = None, db_path: Optional[str] = None) -> int:
    db_path = db_path or ENGRAM_DB_PATH
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    cur.execute(INSERT_MEMORY_SQL, (what, why, where, learned, session_id, confidence, domain))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid


def list_memories(limit: int = 100, db_path: Optional[str] = None) -> List[Dict]:
    db_path = db_path or ENGRAM_DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(SELECT_ALL_SQL, (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def search_memories(query: str, limit: int = 20, db_path: Optional[str] = None) -> List[Dict]:
    db_path = db_path or ENGRAM_DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(SEARCH_FTS_SQL, (query, limit))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def clean_old_memories(days: int = 90, db_path: Optional[str] = None) -> int:
    """
    Elimina memorias antiguas de la base de datos.

    Args:
        days: Número de días de antigüedad para considerar como "antiguas"
        db_path: Ruta opcional a la base de datos

    Returns:
        Número de memorias eliminadas
    """
    db_path = db_path or ENGRAM_DB_PATH

    # Calcular fecha límite
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Contar antes de eliminar
    cur.execute('SELECT COUNT(*) FROM cognitive_stack WHERE timestamp < ?', (cutoff_str,))
    count_before = cur.fetchone()[0]

    # Eliminar memorias antiguas
    cur.execute('DELETE FROM cognitive_stack WHERE timestamp < ?', (cutoff_str,))

    # Los triggers FTS se encargarán de limpiar cognitive_stack_fts automáticamente
    conn.commit()
    conn.close()

    return count_before


if __name__ == '__main__':
    print('Inicializando base de datos Engram en', init_db())
    print('Memoria inicial añadida (ejemplo) ID=', add_memory(
        what='Validación de capa Engram',
        why='Comprobar que la API CRUD funciona',
        where='engram_storage.py',
        learned='API de persistencia local lista para integrar',
        session_id='setup-0001',
        confidence=1.0,
        domain='architecture'
    ))
    print('Memorias recientes:', len(list_memories(5)))
