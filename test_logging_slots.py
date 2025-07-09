#!/usr/bin/env python3
"""
Script para probar los logs mejorados de get_slots_optimized.
"""

import logging
import sys
import os

# Configurar logging para ver los logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_slots_logging.log')
    ]
)

def test_slots_logging():
    """
    Prueba los logs de get_slots_optimized con parámetros de ejemplo.
    """
    print("🧪 Probando logs de get_slots_optimized")
    print("=" * 60)
    
    try:
        # Importar la función después de configurar logging
        from actions.rebooking_actions import get_slots_optimized
        
        # Parámetros de prueba
        test_params = {
            "resource_id": "7dbd3ae4-4ead-4fcf-a131-a5fa005e35a5",
            "service_id": "3229b16d-fa44-4a1e-84ea-a60b014e94ed",
            "coverage_plan_id": "f2d3cd94-b91c-420e-9ec0-a5f800ca8dbc",
            "start_time": "2025-07-08T16:21:01-04:00",
            "finish_time": "2025-07-09T23:59:59-04:00",
            "adjacent_slots": 1,
            "patient_id": "7f8c4c23-7b19-44cb-b964-a60900507f49",
            "include_self_payer": False,
            "expert_booking_mode": False,
            "include_not_bookable": False,
            "reschedule_appointment_id": "9395e3ed-1716-4920-80c4-b2c8010cb692",
            "app_timezone": -240,
            "auth_token": "pkiALQixUCgj1LrLz0fpC7NiMUoJ"
        }
        
        print("📋 Parámetros de prueba:")
        for key, value in test_params.items():
            print(f"   {key}: {value}")
        
        print("\n" + "=" * 60)
        print("🚀 Llamando get_slots_optimized...")
        print("📝 Los logs detallados aparecerán a continuación:")
        print("=" * 60)
        
        # Llamar a la función
        result = get_slots_optimized(**test_params)
        
        print("\n" + "=" * 60)
        print("📊 Resultado de la llamada:")
        
        if result:
            print("✅ Función ejecutada exitosamente")
            if "slots" in result:
                slots_count = len(result["slots"])
                available_count = len([s for s in result["slots"] if s.get("Bookable", {}).get("Bookable", False)])
                print(f"   Total de slots: {slots_count}")
                print(f"   Slots disponibles: {available_count}")
                print(f"   Slots no disponibles: {slots_count - available_count}")
            else:
                print("   Respuesta sin slots")
                print(f"   Claves en respuesta: {list(result.keys())}")
        else:
            print("❌ Función retornó None")
        
        print("\n" + "=" * 60)
        print("✅ Prueba de logging completada")
        print("📄 Revisa el archivo 'test_slots_logging.log' para ver los logs completos")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_slots_logging() 