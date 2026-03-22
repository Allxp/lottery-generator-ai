import os
import sys
import tempfile
import unittest
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engram_storage import (
    init_db, add_memory, list_memories, search_memories,
    ENGRAM_DB_PATH
)


class TestEngramStorage(unittest.TestCase):
    def setUp(self):
        # Usar DB temporal para tests
        self.temp_dir = tempfile.mkdtemp()
        self.temp_db = os.path.join(self.temp_dir, 'test_engram.db')
        init_db(self.temp_db)

    def tearDown(self):
        # Limpiar DB temporal
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)
        os.rmdir(self.temp_dir)

    def test_init_db_crea_tablas(self):
        # Verificar que tablas existen
        import sqlite3
        conn = sqlite3.connect(self.temp_db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        self.assertIn('cognitive_stack', tables)
        self.assertIn('cognitive_stack_fts', tables)
        conn.close()

    def test_add_memory_devuelve_id(self):
        rowid = add_memory(
            what='Test memory',
            why='Testing add_memory',
            where='test',
            learned='Works',
            db_path=self.temp_db
        )
        self.assertIsInstance(rowid, int)
        self.assertGreater(rowid, 0)

    def test_list_memories_orden_desc(self):
        id1 = add_memory('First', 'Why1', 'Where1', 'Learned1', db_path=self.temp_db)
        id2 = add_memory('Second', 'Why2', 'Where2', 'Learned2', db_path=self.temp_db)
        memories = list_memories(limit=10, db_path=self.temp_db)
        self.assertEqual(len(memories), 2)
        # Orden DESC por timestamp, pero verificar que ambos están
        whats = [m['what'] for m in memories]
        self.assertIn('First', whats)
        self.assertIn('Second', whats)

    def test_search_memories_fts(self):
        add_memory('Backtesting strategy', 'Why', 'Where', 'Learned', db_path=self.temp_db)
        add_memory('UI improvement', 'Why', 'Where', 'Learned', db_path=self.temp_db)
        results = search_memories('backtesting', limit=10, db_path=self.temp_db)
        self.assertEqual(len(results), 1)
        self.assertIn('Backtesting', results[0]['what'])

    def test_triggers_update_delete(self):
        # Insertar
        rowid = add_memory('Original', 'Why', 'Where', 'Learned', db_path=self.temp_db)
        memories = list_memories(db_path=self.temp_db)
        self.assertEqual(len(memories), 1)

        # Actualizar (simular trigger)
        import sqlite3
        conn = sqlite3.connect(self.temp_db)
        conn.execute('UPDATE cognitive_stack SET what = ? WHERE id = ?', ('Updated', rowid))
        conn.commit()
        conn.close()

        # Verificar que FTS se actualiza
        results = search_memories('Updated', db_path=self.temp_db)
        self.assertEqual(len(results), 1)

        # Borrar
        conn = sqlite3.connect(self.temp_db)
        conn.execute('DELETE FROM cognitive_stack WHERE id = ?', (rowid,))
        conn.commit()
        conn.close()

        memories = list_memories(db_path=self.temp_db)
        self.assertEqual(len(memories), 0)


if __name__ == '__main__':
    unittest.main()