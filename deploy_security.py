#!/usr/bin/env python3
"""
Script de despliegue para configurar Security Review en GitHub
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecutar comando y mostrar resultado."""
    print(f"\n🔧 {description}")
    print(f"Comando: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=PROJECT_DIR)
        if result.returncode == 0:
            print("✅ Éxito")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print("❌ Error:")
            print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

    return True

def main():
    print("🚀 Asistente de Despliegue: Security Review Automático")
    print("=" * 60)

    # Verificar que estamos en el directorio correcto
    if not Path(".github/workflows/security.yml").exists():
        print("❌ Error: No se encuentra .github/workflows/security.yml")
        print("Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)

    # Verificar estado de Git
    if not run_command("git status --porcelain", "Verificando estado del repositorio"):
        print("❌ El repositorio no está limpio. Confirma tus cambios primero.")
        sys.exit(1)

    # Verificar rama main
    if not run_command("git branch --show-current", "Verificando rama actual"):
        sys.exit(1)

    print("\n📋 PASOS MANUALES REQUERIDOS:")
    print("=" * 40)

    print("\n1️⃣ CREAR REPOSITORIO EN GITHUB:")
    print("   - Ve a https://github.com/new")
    print("   - Nombre: lottery-generator (o el que prefieras)")
    print("   - Crea el repositorio vacío")

    print("\n2️⃣ CONFIGURAR REMOTO:")
    print("   - Copia la URL de tu repositorio")
    print("   - Ejecuta:")
    print("     git remote add origin https://github.com/TU_USUARIO/TU_REPO.git")

    print("\n3️⃣ PUSH INICIAL:")
    print("   git push -u origin main")

    print("\n4️⃣ CONFIGURAR SECRET:")
    print("   - Ve a Settings → Secrets and variables → Actions")
    print("   - New repository secret:")
    print("     Name: ANTHROPIC_API_KEY")
    print("     Value: [tu_api_key_de_anthropic]")

    print("\n5️⃣ PROBAR SECURITY REVIEW:")
    print("   git push origin feature/security-test")
    print("   - Crea un PR desde feature/security-test hacia main")
    print("   - El workflow se activará automáticamente")

    print("\n📖 LEE DEPLOYMENT_SECURITY.md PARA INSTRUCCIONES DETALLADAS")

    print("\n🎯 RESULTADO ESPERADO:")
    print("   - Workflow falla inicialmente (vulnerabilidades detectadas)")
    print("   - Comentarios detallados en el PR")
    print("   - Status check bloquea el merge")

    print("\n✅ UNA VEZ CONFIGURADO:")
    print("   - Todo PR hacia main será auditado automáticamente")
    print("   - Seguridad por diseño garantizada")

    # Confirmación
    input("\n🔄 Presiona Enter cuando hayas completado los pasos manuales...")

    print("\n🎉 ¡Security Review Automático configurado!")
    print("Tu generador de lotería ahora tiene protección integrada contra vulnerabilidades.")

if __name__ == "__main__":
    PROJECT_DIR = Path(__file__).parent
    main()