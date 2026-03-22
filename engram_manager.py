import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

from engram_storage import (
    init_db, list_memories, search_memories, ENGRAM_DB_PATH
)


def cmd_init(args):
    """Inicializar la base de datos Engram."""
    db_path = init_db()
    print(f"Base de datos inicializada en: {db_path}")


def cmd_status(args):
    """Mostrar estado de la base de datos."""
    if not os.path.exists(ENGRAM_DB_PATH):
        print("Base de datos no existe. Ejecuta 'init' primero.")
        return

    memories = list_memories(limit=1000)
    print(f"Total de memorias: {len(memories)}")
    domains = {}
    for m in memories:
        domain = m.get('domain', 'unknown')
        domains[domain] = domains.get(domain, 0) + 1
    print("Por dominio:")
    for domain, count in domains.items():
        print(f"  {domain}: {count}")

    if memories:
        print(f"Última memoria: {memories[0]['timestamp']} - {memories[0]['what']}")


def cmd_backup(args):
    """Crear backup de la base de datos."""
    if not os.path.exists(ENGRAM_DB_PATH):
        print("Base de datos no existe.")
        return

    backup_dir = Path(ENGRAM_DB_PATH).parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f'engram_backup_{timestamp}.db'
    shutil.copy2(ENGRAM_DB_PATH, backup_path)
    print(f"Backup creado: {backup_path}")


def cmd_search(args):
    """Buscar memorias por query FTS."""
    if not os.path.exists(ENGRAM_DB_PATH):
        print("Base de datos no existe.")
        return

    results = search_memories(args.query, limit=args.limit)
    if not results:
        print("No se encontraron resultados.")
        return

    for r in results:
        print(f"[{r['id']}] {r['timestamp']} - {r['what']} (conf: {r['confidence']})")
        print(f"  Why: {r['why']}")
        print(f"  Learned: {r['learned']}")
        print()


def cmd_purge(args):
    """Purgar memorias antiguas (no implementado aún)."""
    print("Purge no implementado. Usa SQL manualmente.")


def main():
    parser = argparse.ArgumentParser(description='CLI para gestión de Engram')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # init
    subparsers.add_parser('init', help='Inicializar base de datos')

    # status
    subparsers.add_parser('status', help='Mostrar estado')

    # backup
    subparsers.add_parser('backup', help='Crear backup')

    # search
    search_parser = subparsers.add_parser('search', help='Buscar memorias')
    search_parser.add_argument('query', help='Query de búsqueda FTS')
    search_parser.add_argument('--limit', type=int, default=20, help='Límite de resultados')

    # purge (placeholder)
    purge_parser = subparsers.add_parser('purge', help='Purgar memorias antiguas')
    purge_parser.add_argument('--older-than', type=int, default=365, help='Días')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        'init': cmd_init,
        'status': cmd_status,
        'backup': cmd_backup,
        'search': cmd_search,
        'purge': cmd_purge,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()