#!/usr/bin/env python3
"""
Script de prueba para el SQL Agent Backend
Prueba la traducción de lenguaje natural a SQL
"""

import requests
import json
import sys

# Configuración
BACKEND_URL = "http://localhost:5000"

def print_separator():
    print("=" * 60)

def test_health():
    """Probar que el servicio esté funcionando"""
    print("🔍 Probando conectividad del servicio...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health/basic", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servicio funcionando: {data['service']}")
            print(f"   Proveedor: {data['provider']}")
            return True
        else:
            print(f"❌ Error en health check: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ No se puede conectar al servicio: {e}")
        return False

def test_sql_generation(query):
    """Probar generación de SQL para una consulta"""
    print(f"\n📝 Consulta: '{query}'")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate-sql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SQL generado exitosamente:")
            print(f"   📊 SQL: {data.get('sql_query', 'No disponible')}")
            
            if 'llm_info' in data:
                llm_info = data['llm_info']
                print(f"   🤖 Modelo: {llm_info.get('model', 'Desconocido')}")
                print(f"   🏪 Proveedor: {llm_info.get('provider', 'Desconocido')}")
            
            if 'validation' in data and data['validation']:
                validation = data['validation']
                print(f"   ✅ Válida: {validation.get('is_valid', False)}")
                if validation.get('warnings'):
                    print(f"   ⚠️  Advertencias: {validation['warnings']}")
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
            print(f"❌ Error {response.status_code}: {error_data.get('detail', error_data.get('error', 'Error desconocido'))}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - El modelo tardó demasiado en responder")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except json.JSONDecodeError:
        print("❌ Error al decodificar la respuesta JSON")

def main():
    """Función principal del script de prueba"""
    print("🚀 Script de Prueba SQL Agent")
    print_separator()
    
    # Verificar conectividad
    if not test_health():
        print("\n❌ El servicio no está disponible. Asegúrate de que esté corriendo:")
        print("   docker-compose up python-backend")
        sys.exit(1)
    
    print_separator()
    
    # Consultas de prueba
    test_queries = [
        "los 5 clientes que más han gastado",
        "lista las 5 películas más alquiladas",
        "total de ingresos por tienda. Muestra las primeras 3 tiendas",
        "actores que aparecen en más de 20 películas"
    ]

    #SELECT * FROM actor LIMIT 10;
    
    print("🧪 Probando generación de SQL...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Prueba {i}/{len(test_queries)} ---")
        test_sql_generation(query)
        
        # Pausa entre consultas para no sobrecargar
        if i < len(test_queries):
            import time
            time.sleep(1)
    
    print_separator()
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main()