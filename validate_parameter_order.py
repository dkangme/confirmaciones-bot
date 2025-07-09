#!/usr/bin/env python3
"""
Script para validar específicamente el orden de los parámetros en la función get_slots_optimized.
"""

import urllib.parse

def validate_parameter_order():
    """
    Valida que el orden de los parámetros en la función es correcto.
    """
    print("🔍 Validando orden de parámetros")
    print("=" * 60)
    
    # Parámetros del curl de ejemplo
    curl_params = {
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
    
    print("📋 Parámetros de entrada:")
    for key, value in curl_params.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    
    # Orden esperado según el curl
    expected_order = [
        "includeSelfPayer=false",
        "expertBookingMode=false", 
        "includeNotBookable=false",
        "rescheduleAppointmentId=9395e3ed-1716-4920-80c4-b2c8010cb692"
    ]
    
    print("🎯 Orden esperado (del curl):")
    for i, param in enumerate(expected_order, 1):
        print(f"   {i}. {param}")
    
    print("\n" + "=" * 60)
    
    # Generar parámetros usando la lógica de la función
    base_url = "https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized"
    
    # Construir parámetros de la URL (corresponden a los parámetros de función en el curl)
    # Orden correcto según el curl: includeSelfPayer, expertBookingMode, includeNotBookable, rescheduleAppointmentId
    params = {
        "includeSelfPayer": str(curl_params["include_self_payer"]).lower(),
        "expertBookingMode": str(curl_params["expert_booking_mode"]).lower(),
        "includeNotBookable": str(curl_params["include_not_bookable"]).lower()
    }
    
    if curl_params["reschedule_appointment_id"]:
        params["rescheduleAppointmentId"] = curl_params["reschedule_appointment_id"]
    
    # Generar lista de parámetros en el orden que se usarían
    generated_params = []
    for key, value in params.items():
        generated_params.append(f"{key}={value}")
    
    print("🔧 Orden generado por la función:")
    for i, param in enumerate(generated_params, 1):
        print(f"   {i}. {param}")
    
    print("\n" + "=" * 60)
    
    # Comparar órdenes
    print("📊 Comparación de órdenes:")
    
    if len(expected_order) == len(generated_params):
        print("✅ Número de parámetros coincide")
        
        all_match = True
        for i, (expected, generated) in enumerate(zip(expected_order, generated_params)):
            if expected == generated:
                print(f"   ✅ Parámetro {i+1}: {expected}")
            else:
                print(f"   ❌ Parámetro {i+1}:")
                print(f"      Esperado: {expected}")
                print(f"      Generado: {generated}")
                all_match = False
        
        if all_match:
            print("\n✅ ¡PERFECTO! El orden de parámetros es correcto")
        else:
            print("\n❌ El orden de parámetros NO es correcto")
    else:
        print(f"❌ Número de parámetros diferente:")
        print(f"   Esperados: {len(expected_order)}")
        print(f"   Generados: {len(generated_params)}")
    
    print("\n" + "=" * 60)
    
    # Verificar nombres específicos
    print("🔍 Verificación de nombres de parámetros:")
    
    name_checks = [
        ("includeSelfPayer", "includeSelfPayer"),
        ("expertBookingMode", "expertBookingMode"), 
        ("includeNotBookable", "includeNotBookable"),
        ("rescheduleAppointmentId", "rescheduleAppointmentId")
    ]
    
    for expected_name, actual_name in name_checks:
        if expected_name in params:
            print(f"   ✅ {expected_name}: Correcto")
        else:
            print(f"   ❌ {expected_name}: No encontrado")
    
    print("\n" + "=" * 60)
    print("✅ Validación de orden completada")


if __name__ == "__main__":
    validate_parameter_order() 