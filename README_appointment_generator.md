# Appointment JSON Generator

Aplicación para generar JSON de rebooking a partir de `appointment_id` desde la base de datos PostgreSQL.

## Descripción

Esta aplicación se conecta a la base de datos del bot de confirmaciones de RedSalud, busca un registro por `appointment_id` y genera el JSON específico requerido para el intent `EXTERNAL_init_rebooking`.

## Características

- ✅ Conexión directa a PostgreSQL
- ✅ Mapeo automático de campos de BD a entidades
- ✅ Generación de JSON estructurado
- ✅ Manejo de errores robusto
- ✅ Logging detallado
- ✅ Valores por defecto para campos faltantes

## Estructura del JSON Generado

```json
{
  "name": "EXTERNAL_init_rebooking",
  "entities": {
    // Datos existentes (mapeados desde BD)
    "nombre_paciente": "Dennis",
    "id_especialidad": "9da27b49-fe81-4188-ba06-b13100fee18d",
    "especialidad": "1° CONSULTA BARIÁTRICA",
    "fecha_hora": "2025-03-18 09:00:00",
    "id_centro_medico": "223ce757-0a28-471b-a13a-a8ac010e5041",
    "centro_medico": "Clínica RedSalud Santiago",
    "centro_medico_address": "",
    "centro_medico_google": "",
    "centro_medico_comuna": "",
    "area_medica": "Médica",
    "bot_name": "Ricardo",
    "campaign_name": "confirmacion",
    "phone_number": "+56956196028",
    "preparations": false,
    "conversation_id": "8fcf10cb-614d-4aa9-8720-b2a300fd978b",
    "preparations_url": "https://www.google.cl",
    "preparation_pdf_name": "prepararions.pdf",
    "resource_name": "Miguel Angulo",
    "resource_id": "5fd72551-58ff-4f12-b144-a5fa00690a42",
    
    // DATOS CRÍTICOS (mapeados desde BD)
    "patient_id": "27a1bd0d-2028-4191-887c-acc9014582a9",
    "service_id": "7c8871ba-36be-47b9-bf9a-a602010902b0",
    "coverage_plan_id": "f2d3cd94-b91c-420e-9ec0-a5f800ca8dbc",
    "starting_location_id": "c7e1f17b-45c6-45e0-b981-a5f800212bef",
    "original_appointment_id": "appointment_id_to_cancel",
    "maximum_distance": 5,
    "adjacent_slots": 1,
    "app_timezone": -240,
    "include_self_payer": false,
    "expert_booking_mode": false,
    "include_not_bookable": true,
    "reschedule_appointment_id": null
  }
}
```

## Mapeo de Campos

| Campo BD | Entidad JSON | Descripción |
|----------|--------------|-------------|
| `patient_full_name` | `nombre_paciente` | Nombre completo del paciente |
| `service_specialty_id` | `id_especialidad` | ID de la especialidad |
| `service_specialty_name` | `especialidad` | Nombre de la especialidad |
| `date_time_from` | `fecha_hora` | Fecha y hora de la cita |
| `center_id` | `id_centro_medico` | ID del centro médico |
| `center_name` | `centro_medico` | Nombre del centro médico |
| `service_area_name` | `area_medica` | Área médica |
| `patient_main_phone_number` | `phone_number` | Teléfono del paciente |
| `appointment_id` | `conversation_id` | ID de la conversación |
| `resource_name` | `resource_name` | Nombre del doctor |
| `resource_id` | `resource_id` | ID del doctor |
| `patient_id` | `patient_id` | ID del paciente |
| `service_id` | `service_id` | ID del servicio |
| `coverage_plan_id` | `coverage_plan_id` | ID del plan de cobertura |

## Uso

### Línea de Comandos

```bash
# Generar JSON para un appointment_id específico
python appointment_json_generator.py 44191913-9766-4848-a195-b31001310d93
```

### Como Módulo Python

```python
from appointment_json_generator import AppointmentJSONGenerator

# Crear instancia
generator = AppointmentJSONGenerator()

# Procesar appointment_id
result = generator.process_appointment_id("44191913-9766-4848-a195-b31001310d93")

if result:
    print(json.dumps(result, indent=2))
```

### Script de Prueba

```bash
# Ejecutar script de prueba
python test_appointment_generator.py
```

## Configuración

### Variables de Entorno

La aplicación utiliza las siguientes variables de entorno (definidas en `.env`):

```bash
DB_HOST=34.45.109.62
DB_USER=bot_client
DB_PORT=5432
DB_PASSWORD=Cg:m8mY=xZR?LB#*
DB_NAME=bot
```

### Dependencias

```bash
pip install psycopg2-binary python-dotenv
```

## Valores por Defecto

Para campos que no están disponibles en la base de datos, se utilizan los siguientes valores por defecto:

- `bot_name`: "Ricardo"
- `campaign_name`: "confirmacion"
- `preparations`: false
- `preparations_url`: "https://www.google.cl"
- `preparation_pdf_name`: "prepararions.pdf"
- `maximum_distance`: 5
- `adjacent_slots`: 1
- `app_timezone`: -240
- `include_self_payer`: false
- `expert_booking_mode`: false
- `include_not_bookable`: true
- `reschedule_appointment_id`: null

## Manejo de Errores

La aplicación maneja los siguientes errores:

- ❌ **Appointment no encontrado**: Si el `appointment_id` no existe en la BD
- ❌ **Error de conexión**: Si no se puede conectar a PostgreSQL
- ❌ **Error de consulta**: Si hay problemas con la consulta SQL
- ❌ **Error de generación**: Si hay problemas al generar el JSON

## Logging

La aplicación genera logs detallados que incluyen:

- ✅ Conexión exitosa a la base de datos
- ✅ Registro encontrado/no encontrado
- ✅ JSON generado exitosamente
- ❌ Errores de conexión, consulta o generación

## Ejemplo de Salida

```bash
$ python appointment_json_generator.py 44191913-9766-4848-a195-b31001310d93

2025-01-27 10:30:15 - __main__ - INFO - Registro encontrado para appointment_id: 44191913-9766-4848-a195-b31001310d93
2025-01-27 10:30:15 - __main__ - INFO - JSON de rebooking generado exitosamente
{
  "name": "EXTERNAL_init_rebooking",
  "entities": {
    "nombre_paciente": "Dennis",
    "id_especialidad": "9da27b49-fe81-4188-ba06-b13100fee18d",
    "especialidad": "1° CONSULTA BARIÁTRICA",
    "fecha_hora": "2025-03-18 09:00:00",
    "id_centro_medico": "223ce757-0a28-471b-a13a-a8ac010e5041",
    "centro_medico": "Clínica RedSalud Santiago",
    "centro_medico_address": "",
    "centro_medico_google": "",
    "centro_medico_comuna": "",
    "area_medica": "Médica",
    "bot_name": "Ricardo",
    "campaign_name": "confirmacion",
    "phone_number": "+56956196028",
    "preparations": false,
    "conversation_id": "44191913-9766-4848-a195-b31001310d93",
    "preparations_url": "https://www.google.cl",
    "preparation_pdf_name": "prepararions.pdf",
    "resource_name": "Miguel Angulo",
    "resource_id": "5fd72551-58ff-4f12-b144-a5fa00690a42",
    "patient_id": "27a1bd0d-2028-4191-887c-acc9014582a9",
    "service_id": "7c8871ba-36be-47b9-bf9a-a602010902b0",
    "coverage_plan_id": "f2d3cd94-b91c-420e-9ec0-a5f800ca8dbc",
    "starting_location_id": "223ce757-0a28-471b-a13a-a8ac010e5041",
    "original_appointment_id": "44191913-9766-4848-a195-b31001310d93",
    "maximum_distance": 5,
    "adjacent_slots": 1,
    "app_timezone": -240,
    "include_self_payer": false,
    "expert_booking_mode": false,
    "include_not_bookable": true,
    "reschedule_appointment_id": null
  }
}
```

## Integración con el Bot

Este JSON generado puede ser utilizado directamente en el bot de Rasa para:

1. **Inicializar contexto de rebooking**: Enviar el JSON al bot para iniciar el flujo de reagendamiento
2. **Testing**: Probar el flujo de rebooking con datos reales
3. **Debugging**: Verificar que todos los campos necesarios estén presentes
4. **Desarrollo**: Generar datos de prueba para desarrollo

## Notas Técnicas

- **Conexión**: Usa `psycopg2` para conexión directa a PostgreSQL
- **Mapeo**: Mapea automáticamente campos de BD a entidades del JSON
- **Valores por defecto**: Proporciona valores seguros para campos faltantes
- **Logging**: Genera logs detallados para debugging
- **Error handling**: Maneja errores de forma robusta 