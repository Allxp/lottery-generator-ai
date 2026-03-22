#!/usr/bin/env python3
"""
Archivo de prueba para validar el Security Review automático.
Este archivo contiene vulnerabilidades intencionales para testing.
"""

import sqlite3

def vulnerable_sql_injection(user_input):
    """Función con SQL injection intencional para testing."""
    conn = sqlite3.connect('data/engram.db')
    cursor = conn.cursor()

    # VULNERABILIDAD: SQL Injection - No usar f-strings en SQL
    query = f"SELECT * FROM cognitive_stack WHERE what LIKE '%{user_input}%'"
    cursor.execute(query)  # Esto es peligroso!

    results = cursor.fetchall()
    conn.close()
    return results

def exposed_secret():
    """Función que expone un secret intencional para testing."""
    # VULNERABILIDAD: Hardcoded secret
    api_key = "sk-ant-api03-1234567890abcdef"  # Esto nunca debería estar en código
    database_password = "super_secret_password_123"

    print(f"API Key: {api_key}")  # Exposición de secret
    print(f"DB Password: {database_password}")

    return api_key

def test_leidsa_corruption():
    """Función que simula corrupción de datos LEIDSA para testing."""
    # VULNERABILIDAD: Lógica que podría corromper estadísticas
    historical_data = [1, 2, None, 4, 5]  # Datos históricos con nulls

    # Procesamiento incorrecto que ignora nulls sin validación
    processed = [x for x in historical_data if x is not None]
    average = sum(processed) / len(processed) if processed else 0

    # Esto podría corromper estadísticas si no se maneja correctamente
    return average

if __name__ == "__main__":
    print("🧪 Archivo de prueba para Security Review")
    print("Este archivo contiene vulnerabilidades intencionales:")
    print("1. SQL Injection en vulnerable_sql_injection()")
    print("2. Secrets expuestos en exposed_secret()")
    print("3. Posible corrupción de datos LEIDSA en test_leidsa_corruption()")