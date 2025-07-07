#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad EXTERNAL_init_context.
Simula el envío de un mensaje con la intención y entidades especificadas.
"""

import json
import requests
import time
from typing import Dict, Any

# Configuración del servidor RASA
RASA_URL = "http://localhost:5005"
ACTIONS_URL = "http://localhost:5055"

def test_external_init_context():
    """
    Prueba la funcionalidad EXTERNAL_init_context enviando un mensaje con entidades.
    """
    
    # Datos de prueba basados en el ejemplo proporcionado
    test_data = {
        "sender": "test_user",
        "message": "init context",
        "entities": [
            {"entity": "nombre_paciente", "value": "Manuel Castillo Vicuña"},
            {"entity": "id_especialidad", "value": "d76fee22-6a38-43ef-b824-a60d001fe940"},
            {"entity": "especialidad", "value": "MEDICINA GENERAL ADULTO"},
            {"entity": "fecha_hora", "value": "2025-07-02T19:00:00-04:00"},
            {"entity": "id_centro_medico", "value": "c7e1f17b-45c6-45e0-b981-a5f800212bef"},
            {"entity": "centro_medico", "value": "RedSalud Alameda"},
            {"entity": "centro_medico_address", "value": "San Martin 30 ,Santiago"},
            {"entity": "centro_medico_google", "value": "https://goo.gl/maps/T7iNCdZcQc35gbp58"},
            {"entity": "centro_medico_comuna", "value": "Santiago"},
            {"entity": "area_medica", "value": "Médica"},
            {"entity": "conversation_id", "value": "70fc2fdd-1721-4439-bf6e-b30e010acec7"},
            {"entity": "bot_name", "value": "BOT DEV"},
            {"entity": "campaign_name", "value": "confirmacion"},
            {"entity": "phone_number", "value": "+56964058510"},
            {"entity": "preparations", "value": True},
            {"entity": "tipo_mensaje", "value": "Confirmacion"},
            {"entity": "centro_medico_tipo", "value": "Clínica"},
            {"entity": "preparation_url", "value": "https://drive.google.com/file/d/13-7QlkXRg3-lVsDCe0LCdVDhw3FsJfAS/view?usp=drive_link"},
            {"entity": "preparation_pdf_name", "value": None},
            {"entity": "resource_name", "value": "Celeste Olivia Borie Polanco"},
            {"entity": "status", "value": "ready to send"},
            {"entity": "piso", "value": None},
            {"entity": "torre", "value": None},
            {"entity": "autopago", "value": None}
        ]
    }
    
    print("🧪 Iniciando prueba de EXTERNAL_init_context...")
    print(f"📡 Enviando mensaje a: {RASA_URL}/webhooks/rest/webhook")
    print(f"📋 Entidades a procesar: {len(test_data['entities'])}")
    
    try:
        # Enviar mensaje al webhook de RASA
        response = requests.post(
            f"{RASA_URL}/webhooks/rest/webhook",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Respuesta recibida exitosamente")
            print(f"📊 Número de respuestas: {len(result)}")
            
            for i, message in enumerate(result, 1):
                print(f"\n📝 Respuesta {i}:")
                print(f"   Texto: {message.get('text', 'N/A')}")
                print(f"   Recipient: {message.get('recipient_id', 'N/A')}")
                
                # Verificar si la respuesta indica que el contexto se inicializó
                if "Contexto Inicializado" in message.get('text', ''):
                    print("🎉 ¡ÉXITO! El contexto se inicializó correctamente")
                elif "confirmación" in message.get('text', ''):
                    print("🎉 ¡ÉXITO! Se detectó la palabra 'confirmación' en la respuesta")
                    
        else:
            print(f"❌ Error en la respuesta: {response.status_code}")
            print(f"   Contenido: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor RASA")
        print("   Asegúrate de que el servidor esté ejecutándose con: rasa run --enable-api --cors '*'")
    except requests.exceptions.Timeout:
        print("❌ Error de timeout: La solicitud tardó demasiado")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")


def test_simple_message():
    """
    Prueba un mensaje simple para verificar que el bot responde.
    """
    
    test_data = {
        "sender": "test_user",
        "message": "hello"
    }
    
    print("\n🧪 Probando mensaje simple...")
    
    try:
        response = requests.post(
            f"{RASA_URL}/webhooks/rest/webhook",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Respuesta simple recibida")
            for message in result:
                print(f"   Texto: {message.get('text', 'N/A')}")
        else:
            print(f"❌ Error en respuesta simple: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en prueba simple: {str(e)}")


def check_server_status():
    """
    Verifica el estado del servidor RASA.
    """
    
    print("🔍 Verificando estado del servidor...")
    
    try:
        # Verificar servidor principal
        response = requests.get(f"{RASA_URL}/status", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor RASA principal: Activo")
        else:
            print(f"⚠️  Servidor RASA principal: Estado {response.status_code}")
    except:
        print("❌ Servidor RASA principal: No disponible")
    
    try:
        # Verificar servidor de acciones
        response = requests.get(f"{ACTIONS_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor de acciones: Activo")
        else:
            print(f"⚠️  Servidor de acciones: Estado {response.status_code}")
    except:
        print("❌ Servidor de acciones: No disponible")


def main():
    """
    Función principal de pruebas.
    """
    print("🚀 Iniciando pruebas de EXTERNAL_init_context")
    print("=" * 50)
    
    # Verificar estado del servidor
    check_server_status()
    print()
    
    # Probar mensaje simple primero
    test_simple_message()
    print()
    
    # Probar funcionalidad principal
    test_external_init_context()
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")


if __name__ == "__main__":
    main() 