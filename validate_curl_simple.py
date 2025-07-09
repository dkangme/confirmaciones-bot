#!/usr/bin/env python3
"""
Script simplificado para validar que la función get_slots_optimized genera la misma URL que el curl proporcionado.
"""

import urllib.parse

def validate_curl_compatibility():
    """
    Valida que la función get_slots_optimized genera la URL correcta.
    """
    print("🔍 Validando compatibilidad con curl")
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
    
    # URL esperada del curl (decodificada)
    expected_url = (
        "https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized"
        "(includeSelfPayer=false,expertBookingMode=false,includeNotBookable=false,rescheduleAppointmentId=9395e3ed-1716-4920-80c4-b2c8010cb692)"
        "?$filter=ResourceId eq 7dbd3ae4-4ead-4fcf-a131-a5fa005e35a5 and ServiceId eq 3229b16d-fa44-4a1e-84ea-a60b014e94ed and CoveragePlanId eq f2d3cd94-b91c-420e-9ec0-a5f800ca8dbc and (StartTime ge 2025-07-08T16:21:01-04:00) and (FinishTime le 2025-07-09T23:59:59-04:00) and AdjacentSlots eq 1 and PatientId eq 7f8c4c23-7b19-44cb-b964-a60900507f49"
        "&$orderby=StartTime asc&$count=true"
    )
    
    print("🎯 URL esperada (del curl):")
    print(f"   {expected_url}")
    
    print("\n" + "=" * 60)
    
    # Generar URL usando la lógica de la función get_slots_optimized
    base_url = "https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized"
    
    # Construir parámetros de la URL (corresponden a los parámetros de función en el curl)
    params = {
        "includeSelfPayer": str(curl_params["include_self_payer"]).lower(),
        "expertBookingMode": str(curl_params["expert_booking_mode"]).lower(),
        "includeNotBookable": str(curl_params["include_not_bookable"]).lower()
    }
    
    if curl_params["reschedule_appointment_id"]:
        params["rescheduleAppointmentId"] = curl_params["reschedule_appointment_id"]
    
    # Construir filtro (corresponde al $filter en el curl)
    filter_parts = [
        f"ResourceId eq {curl_params['resource_id']}",
        f"ServiceId eq {curl_params['service_id']}",
        f"CoveragePlanId eq {curl_params['coverage_plan_id']}",
        f"(StartTime ge {curl_params['start_time']})",
        f"(FinishTime le {curl_params['finish_time']})",
        f"AdjacentSlots eq {curl_params['adjacent_slots']}",
        f"PatientId eq {curl_params['patient_id']}"
    ]
    
    filter_str = " and ".join(filter_parts)
    
    # Construir URL completa (corresponde exactamente al formato del curl)
    # Formato: base_url(param1=value1,param2=value2)?$filter=...&$orderby=...&$count=true
    generated_url = f"{base_url}({','.join(f'{k}={v}' for k, v in params.items())})"
    generated_url += f"?$filter={urllib.parse.quote(filter_str)}"
    generated_url += "&$orderby=StartTime asc&$count=true"
    
    print("🔧 URL generada por la función:")
    print(f"   {generated_url}")
    
    print("\n" + "=" * 60)
    
    # Comparar URLs
    print("📊 Comparación:")
    
    # Decodificar la URL generada para comparar
    decoded_generated = urllib.parse.unquote(generated_url)
    
    print("✅ URLs coinciden en estructura:")
    print(f"   Base URL: {'✅' if base_url in decoded_generated else '❌'}")
    print(f"   Parámetros de función: {'✅' if 'includeSelfPayer=false' in decoded_generated else '❌'}")
    print(f"   Filtro ResourceId: {'✅' if 'ResourceId eq 7dbd3ae4-4ead-4fcf-a131-a5fa005e35a5' in decoded_generated else '❌'}")
    print(f"   Filtro ServiceId: {'✅' if 'ServiceId eq 3229b16d-fa44-4a1e-84ea-a60b014e94ed' in decoded_generated else '❌'}")
    print(f"   Filtro CoveragePlanId: {'✅' if 'CoveragePlanId eq f2d3cd94-b91c-420e-9ec0-a5f800ca8dbc' in decoded_generated else '❌'}")
    print(f"   Filtro StartTime: {'✅' if 'StartTime ge 2025-07-08T16:21:01-04:00' in decoded_generated else '❌'}")
    print(f"   Filtro FinishTime: {'✅' if 'FinishTime le 2025-07-09T23:59:59-04:00' in decoded_generated else '❌'}")
    print(f"   Filtro AdjacentSlots: {'✅' if 'AdjacentSlots eq 1' in decoded_generated else '❌'}")
    print(f"   Filtro PatientId: {'✅' if 'PatientId eq 7f8c4c23-7b19-44cb-b964-a60900507f49' in decoded_generated else '❌'}")
    print(f"   OrderBy: {'✅' if '$orderby=StartTime asc' in decoded_generated else '❌'}")
    print(f"   Count: {'✅' if '$count=true' in decoded_generated else '❌'}")
    
    print("\n" + "=" * 60)
    
    # Comparación directa
    print("🔍 Comparación directa de URLs:")
    if decoded_generated == expected_url:
        print("✅ ¡PERFECTO! Las URLs coinciden exactamente")
    else:
        print("❌ Las URLs NO coinciden exactamente")
        print("\nDiferencias:")
        
        # Comparar por partes
        if base_url not in decoded_generated:
            print("   - Base URL diferente")
        
        # Comparar parámetros de función
        expected_params = "includeSelfPayer=false,expertBookingMode=false,includeNotBookable=false,rescheduleAppointmentId=9395e3ed-1716-4920-80c4-b2c8010cb692"
        generated_params = ",".join(f'{k}={v}' for k, v in params.items())
        if expected_params != generated_params:
            print(f"   - Parámetros de función diferentes:")
            print(f"     Esperado: {expected_params}")
            print(f"     Generado: {generated_params}")
        
        # Comparar filtros
        expected_filter = "ResourceId eq 7dbd3ae4-4ead-4fcf-a131-a5fa005e35a5 and ServiceId eq 3229b16d-fa44-4a1e-84ea-a60b014e94ed and CoveragePlanId eq f2d3cd94-b91c-420e-9ec0-a5f800ca8dbc and (StartTime ge 2025-07-08T16:21:01-04:00) and (FinishTime le 2025-07-09T23:59:59-04:00) and AdjacentSlots eq 1 and PatientId eq 7f8c4c23-7b19-44cb-b964-a60900507f49"
        if expected_filter != filter_str:
            print(f"   - Filtros diferentes:")
            print(f"     Esperado: {expected_filter}")
            print(f"     Generado: {filter_str}")
    
    print("\n" + "=" * 60)
    print("✅ Validación completada")


if __name__ == "__main__":
    validate_curl_compatibility() 