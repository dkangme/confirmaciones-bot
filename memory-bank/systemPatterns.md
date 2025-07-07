# System Patterns: Bot de Confirmaciones RedSalud

## Arquitectura del Sistema

### Componentes Principales
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   Rasa Bot      │    │   RedSalud      │
│   Business API  │◄──►│   (Actions)     │◄──►│   API/Apigee    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   (Logging)     │
                       └─────────────────┘
```

### Flujo de Datos
1. **Entrada**: Mensaje de WhatsApp → Rasa NLU
2. **Procesamiento**: Rasa Core → Actions → API RedSalud
3. **Respuesta**: Actions → Rasa → WhatsApp
4. **Logging**: Todas las operaciones → PostgreSQL

## Patrones de Diseño Implementados

### 1. **Action Pattern**
```python
class ActionCancelAppointment(Action):
    def name(self) -> Text:
        return "action_cancel_appointment"
    
    def run(self, dispatcher, tracker, domain):
        # Lógica de cancelación
        # Manejo de errores
        # Respuesta al usuario
```

### 2. **Fallback Pattern**
```python
class ActionFallback(Action):
    def run(self, dispatcher, tracker, domain):
        # Mensaje de ayuda personalizado
        # Opciones disponibles
        # Guía para el usuario
```

### 3. **Error Handling Pattern**
```python
try:
    # Operación principal
    result = api_call()
    if "error" in result:
        dispatcher.utter_message(response="utter_error")
    else:
        dispatcher.utter_message(response="utter_success")
except Exception as e:
    logger.error(f"Error: {e}")
    dispatcher.utter_message(response="utter_error")
```

### 4. **Configuration Pattern**
```python
# Variables de entorno centralizadas
REDSALUD_CONFIG = {
    "auth_url": os.getenv("APIGEE_API_URL") + "/oauth/token",
    "base_url": os.getenv("APIGEE_API_URL"),
    "client_id": os.getenv("APIGEE_USERNAME"),
    "client_secret": os.getenv("APIGEE_PASSWORD")
}
```

### 5. **Context Management Pattern**
```python
class ActionInitContext(Action):
    def run(self, dispatcher, tracker, domain):
        # Procesar entidades
        # Configurar contexto específico
        # Actualizar slots
        slot_events.append(SlotSet("contexto", "confirmación"))
```

### 6. **Date Processing Pattern**
```python
class ActionProcessDateRequest(Action):
    def _extract_date_time(self, message: str) -> tuple:
        # Extraer fecha y hora de expresiones naturales
        # Formatear en español
        # Generar rangos de tiempo
        return fecha, hora
    
    def _generate_time_range(self, fecha: str, hora: str) -> tuple:
        # Convertir a formato ISO
        # Generar start_time y end_time
        return start_time, end_time
```

### 7. **API Integration Pattern**
```python
def get_slots_optimized(
    resource_id: str,
    service_id: str,
    coverage_plan_id: str,
    start_time: str,
    finish_time: str,
    adjacent_slots: int,
    patient_id: str,
    # ... otros parámetros
) -> Dict:
    # Construir URL con parámetros
    # Llamar API con headers
    # Procesar respuesta
    # Logging detallado
    return response_data
```

### 8. **Slot Correction Pattern**
```python
# Obtener parámetros de los slots correctos
resource_id = get_slot_value(tracker, "resource_id") or get_slot_value(tracker, "resource_name")
patient_id = get_slot_value(tracker, "patient_id")  # Usar slot correcto
service_id = get_slot_value(tracker, "id_especialidad")
```

## Estructura de Archivos

### Core Rasa Files
```
├── domain.yml              # Configuración de intents, entities, slots, responses
├── config.yml              # Pipeline de NLU y políticas de Core
├── data/
│   ├── nlu.yml            # Ejemplos de entrenamiento para intents
│   ├── stories.yml        # Flujos de conversación
│   ├── rules.yml          # Reglas de comportamiento
│   ├── rebooking_nlu.yml  # Ejemplos específicos de rebooking
│   ├── rebooking_stories.yml # Flujos de rebooking
│   └── rebooking_rules.yml   # Reglas de rebooking
└── endpoints.yml          # Configuración de endpoints
```

### Actions
```
├── actions/
│   ├── __init__.py        # Importaciones de acciones
│   ├── actions.py         # Implementación de acciones personalizadas
│   ├── rebooking_actions.py # Acciones específicas de rebooking
│   ├── database.py        # Conexión y operaciones de BD
│   └── utils.py           # Utilidades compartidas
```

### Configuration
```
├── .env                   # Variables de entorno
├── credentials.yml        # Configuración de WhatsApp
├── logging_config.py      # Configuración de logging
└── requirements.txt       # Dependencias de Python
```

## Patrones de Conversación

### 1. **Confirmación de Cita**
```
Usuario: "Sí" (affirm)
Bot: action_confirm_appointment
  ├─ Éxito: utter_confirm_affirm_medica_confirmacion_centro_medico_medicina_general
  └─ Error: utter_confirmation_appointment_failed
```

### 2. **Cancelación de Cita**
```
Usuario: "No" (deny)
Bot: action_cancel_appointment
  ├─ Éxito: utter_confirm_deny
  └─ Error: utter_cancel_appointment_failed
```

### 3. **Reagendamiento de Cita**
```
Usuario: "Sí" (affirm)
Bot: utter_rebooking_confirmed
Usuario: "No" (deny)
Bot: utter_rebooking_cancelled
```

### 4. **Procesamiento de Fecha**
```
Usuario: "mañana a las 10" (proponer_fecha)
Bot: action_process_date_request
  ├─ Extraer fecha y hora
  ├─ Generar start_time y end_time
  ├─ Llamar get_slots_optimized
  └─ Mostrar horarios disponibles
```

### 5. **Selección de Horario**
```
Usuario: "1" (seleccionar_opcion)
Bot: action_process_slot_selection
  ├─ Validar selección
  ├─ Guardar selected_slot
  └─ Confirmar selección
```

### 6. **Confirmación de Rebooking**
```
Usuario: "Sí" (affirm_rebooking_confirm)
Bot: action_confirm_rebooking
  ├─ Confirmar reagendamiento
  ├─ Limpiar slots de rebooking
  └─ Mensaje de éxito
```

### 7. **Fallback**
```
Usuario: "mensaje no entendido"
Bot: action_fallback
  └─ Mensaje de ayuda con opciones
```

## Manejo de Estados

### Slots Principales
- `contexto`: "confirmación" o "rebooking" según el flujo activo
- `contexto_rebooking`: "rebooking" cuando está activo el flujo de reagendamiento
- `fecha_hora_formato`: Fecha formateada en español
- `appointment_id`: ID de la cita para operaciones API
- `nombre_paciente`, `resource_name`, `centro_medico`: Información de la cita

### Slots de Rebooking
- `rebooking_fecha`: Fecha extraída del usuario
- `rebooking_hora`: Hora extraída del usuario
- `start_time`: Tiempo de inicio en formato ISO
- `end_time`: Tiempo de fin en formato ISO
- `available_slots`: Lista de horarios disponibles
- `selected_slot`: Horario seleccionado por el usuario
- `slot_selection_index`: Índice de la selección

### Mapeo de Slots con Tabla `appointments`
| Slot del Bot | Campo de BD | Descripción |
|--------------|-------------|-------------|
| `conversation_id` | `appointment_id` | ID único de la cita (usado como appointment_id) |
| `nombre_paciente` | `patient_full_name` | Nombre completo del paciente |
| `resource_name` | `resource_name` | Nombre del doctor/recurso |
| `centro_medico` | `center_name` | Nombre del centro médico |
| `fecha_hora` | `date_time_from` | Fecha y hora de la cita |
| `especialidad` | `service_specialty_name` | Especialidad médica |
| `area_medica` | `service_area_name` | Área de servicio (medica/dental) |
| `conversation_id` | `campaign_id` | ID de la campaña/conversación |
| `patient_id` | `patient_id` | ID del paciente |
| `patient_phone` | `patient_main_phone_number` | Teléfono del paciente |
| `service_name` | `service_name` | Nombre del servicio |
| `coverage_plan` | `coverage_plan_name` | Plan de cobertura |
| `duration` | `duration` | Duración de la cita |
| `status` | `status` | Estado de la cita |
| `is_confirmed` | `is_confirmed` | Si la cita está confirmada |

### Reglas de Comportamiento
```yaml
- rule: Confirm appointment when user affirms
  condition:
  - slot_was_set:
    - contexto: "confirmación"
  steps:
  - intent: affirm
  - action: action_confirm_appointment

- rule: Cancel appointment when user denies
  condition:
  - slot_was_set:
    - contexto: "confirmación"
  steps:
  - intent: deny
  - action: action_cancel_appointment

- rule: Confirm rebooking when user affirms
  condition:
  - slot_was_set:
    - contexto: "rebooking"
  steps:
  - intent: affirm
  - action: utter_rebooking_confirmed

- rule: Cancel rebooking when user denies
  condition:
  - slot_was_set:
    - contexto: "rebooking"
  steps:
  - intent: deny
  - action: utter_rebooking_cancelled

- rule: Process date request
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: proponer_fecha
  - action: action_process_date_request

- rule: Process slot selection
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: seleccionar_opcion
  - action: action_process_slot_selection

- rule: Confirm rebooking selection
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: affirm_rebooking_confirm
  - action: action_confirm_rebooking
```

## Patrones de API

### 1. **Autenticación OAuth2**
```python
def obtener_access_token():
    # Obtener token de APIGEE
    # Cache para eficiencia
    # Manejo de errores
    return token
```

### 2. **Confirmación de Cita**
```python
def confirm_appointment(appointment_id: str, token: str):
    # POST a /agendarsv2/cita/confirmar/
    # Headers con token
    # Timeout de 90 segundos
    # Logging de respuesta
    return response
```

### 3. **Cancelación de Cita**
```python
def cancel_appointment(appointment_id: str, token: str):
    # POST a /agendarsv2/cita/anular/
    # Headers con token
    # Timeout de 90 segundos
    # Logging de respuesta
    return response
```

### 4. **Obtención de Slots Optimizados**
```python
def get_slots_optimized(
    resource_id: str,
    service_id: str,
    coverage_plan_id: str,
    start_time: str,
    finish_time: str,
    adjacent_slots: int,
    patient_id: str,
    # ... otros parámetros
):
    # Construir URL con filtros
    # GET a /AWAUsers/Slots/GetSlotsOptimized
    # Procesar respuesta JSON
    # Formatear horarios disponibles
    return slots_data
```

## Patrones de Logging

### 1. **Request Logging**
```python
def log_request_info(tracker: Tracker, action_name: str):
    # Log de información de la conversación
    # Log de slots actuales
    # Log de entidades recibidas
```

### 2. **API Response Logging**
```python
# Log de URL generada
logger.info(f"🌐 URL generada para get_slots_optimized:")
logger.info(f"   Base URL: {base_url}")
logger.info(f"   Parámetros: {params}")

# Log de headers (sin token por seguridad)
logger.info(f"📋 Headers de la petición:")
logger.info(f"   Authorization: Bearer [TOKEN_OCULTO]")

# Log de respuesta
logger.info(f"✅ Respuesta exitosa de la API:")
logger.info(f"   Status Code: {response.status_code}")
```

### 3. **Error Logging**
```python
except Exception as e:
    logger.error(f"❌ Error al llamar a la API: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        logger.error(f"   Status Code: {e.response.status_code}")
        logger.error(f"   Response Text: {e.response.text}")
```

## Patrones de Validación

### 1. **Validación de Parámetros**
```python
# Validar parámetros requeridos
required_params = [resource_id, service_id, start_time, end_time, patient_id]
if not all(required_params):
    logger.error(f"Parámetros faltantes para get_slots_optimized: {required_params}")
    return None
```

### 2. **Validación de Slots**
```python
# Verificar que slots existan antes de usarlos
if not get_slot_value(tracker, "appointment_id"):
    dispatcher.utter_message(text="❌ Error: Información incompleta")
    return []
```

### 3. **Validación de Respuestas API**
```python
if response and "error" not in response:
    # Procesar respuesta exitosa
else:
    # Manejar error
    dispatcher.utter_message(response="utter_error")
```

## Flujos de Contexto

### Contexto de Confirmación
1. **Inicialización**: `EXTERNAL_init_context` → `action_init_context`
2. **Configuración**: `contexto = "confirmación"`
3. **Interacción**: `greet` → `utter_greet` (template o botones)
4. **Respuesta**: `affirm` → `action_confirm_appointment` / `deny` → `action_cancel_appointment`

### Contexto de Rebooking
1. **Inicialización**: `EXTERNAL_init_rebooking` → `action_init_rebooking`
2. **Configuración**: `contexto = "rebooking"`
3. **Interacción**: `greet` → `utter_rebooking` (botones interactivos)
4. **Respuesta**: `affirm` → `utter_rebooking_confirmed` / `deny` → `utter_rebooking_cancelled`

### Fallback Contextual
- **Sin contexto**: Respuesta general con opciones disponibles
- **Con contexto**: Respuesta específica según el flujo activo 