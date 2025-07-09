#!/usr/bin/env python3
"""
Script de prueba para demostrar el uso de appointment_json_generator.py
"""

import json
from appointment_json_generator import AppointmentJSONGenerator

def test_appointment_generator():
    """
    Prueba la aplicación con un appointment_id de ejemplo.
    """
    print("🧪 Probando Appointment JSON Generator")
    print("=" * 50)
    
    # Crear instancia del generador
    generator = AppointmentJSONGenerator()
    
    # Appointment ID de ejemplo (usar uno real de tu BD)
    test_appointment_id = "44191913-9766-4848-a195-b31001310d93"
    
    print(f"📋 Procesando appointment_id: {test_appointment_id}")
    print()
    
    # Procesar appointment_id
    result = generator.process_appointment_id(test_appointment_id)
    
    if result:
        print("✅ JSON generado exitosamente:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Mostrar información específica
        entities = result.get('entities', {})
        print("\n📊 Información extraída:")
        print(f"   • Paciente: {entities.get('nombre_paciente', 'N/A')}")
        print(f"   • Especialidad: {entities.get('especialidad', 'N/A')}")
        print(f"   • Centro: {entities.get('centro_medico', 'N/A')}")
        print(f"   • Doctor: {entities.get('resource_name', 'N/A')}")
        print(f"   • Fecha: {entities.get('fecha_hora', 'N/A')}")
        print(f"   • Patient ID: {entities.get('patient_id', 'N/A')}")
        print(f"   • Service ID: {entities.get('service_id', 'N/A')}")
        print(f"   • Coverage Plan ID: {entities.get('coverage_plan_id', 'N/A')}")
        
    else:
        print("❌ Error: No se pudo generar JSON")
        print("💡 Verifica que:")
        print("   • El appointment_id existe en la base de datos")
        print("   • Las credenciales de BD son correctas")
        print("   • La conexión a la BD está disponible")


if __name__ == "__main__":
    test_appointment_generator() 