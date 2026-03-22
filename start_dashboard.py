#!/usr/bin/env python3
"""
Script de inicio para el Dashboard del Generador de Lotería

Uso:
    python start_dashboard.py
    # o simplemente:
    python dashboard.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Verificar que las dependencias necesarias estén instaladas."""
    try:
        import flask
        print("✅ Flask está instalado")
    except ImportError:
        print("❌ Flask no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask instalado correctamente")

def check_database():
    """Verificar que la base de datos Engram existe."""
    db_path = Path("data/engram.db")
    if db_path.exists():
        print(f"✅ Base de datos Engram encontrada: {db_path}")
    else:
        print(f"⚠️  Base de datos no encontrada: {db_path}")
        print("   Ejecuta 'python engram_manager.py init' para inicializar")

def start_dashboard():
    """Iniciar el dashboard."""
    print("🚀 Iniciando Dashboard del Generador de Lotería...")
    print("=" * 60)

    # Verificar dependencias
    check_dependencies()
    print()

    # Verificar base de datos
    check_database()
    print()

    # Iniciar el servidor
    print("🌐 Iniciando servidor web...")
    print("📱 Dashboard disponible en: http://localhost:5000")
    print("❌ Presiona Ctrl+C para detener")
    print()

    try:
        # Ejecutar dashboard.py
        subprocess.run([sys.executable, "dashboard.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_dashboard()