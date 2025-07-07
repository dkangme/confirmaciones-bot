# Tech Context: Bot de Confirmaciones RedSalud

## Stack Tecnológico

### Core Framework
- **Rasa**: 3.6.21 (Framework de chatbot)
- **Rasa SDK**: 3.6.2 (SDK para acciones personalizadas)
- **Python**: 3.8.10 (Lenguaje de programación)

### Base de Datos
- **PostgreSQL**: Base de datos principal
- **psycopg2-binary**: 2.9.7 (Driver de PostgreSQL)

#### Esquema de Base de Datos

##### Tabla `appointments`
```sql
CREATE TABLE "public"."appointments" ( 
  "id" UUID NOT NULL,
  "appointment_id" VARCHAR NOT NULL,
  "status" VARCHAR NULL,
  "date_time_from" VARCHAR NULL,
  "center_id" VARCHAR NULL,
  "coverage_plan_id" VARCHAR NULL,
  "patient_id" VARCHAR NULL,
  "service_id" VARCHAR NULL,
  "created_on" VARCHAR NULL,
  "duration" INTEGER NULL,
  "patient_full_name" VARCHAR NULL,
  "patient_first_name" VARCHAR NULL,
  "patient_last_name" VARCHAR NULL,
  "patient_main_phone_number" VARCHAR NULL,
  "center_name" VARCHAR NULL,
  "resource_id" VARCHAR NULL,
  "resource_name" VARCHAR NULL,
  "coverage_plan_name" VARCHAR NULL,
  "service_name" VARCHAR NULL,
  "service_area_id" VARCHAR NULL,
  "service_area_name" VARCHAR NULL,
  "service_specialty_id" VARCHAR NULL,
  "service_specialty_name" VARCHAR NULL,
  "template" VARCHAR NULL,
  "campaign_id" VARCHAR NULL,
  "patient_document_number" VARCHAR NULL,
  "last_notification_date" TIMESTAMP WITH TIME ZONE NULL,
  "created_at" TIMESTAMP NOT NULL DEFAULT now(),
  "updated_at" TIMESTAMP NOT NULL DEFAULT now(),
  "is_confirmed" BOOLEAN NULL DEFAULT false,
  "appointment_type_id" VARCHAR NULL,
  CONSTRAINT "PK_4a437a9a27e948726b8bb3e36ad" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "idx_appointments_appointment_id" 
ON "public"."appointments" ("appointment_id" ASC);
```

##### Campos Clave de la Tabla `appointments`

###### Identificación
- **`id`**: UUID primario de la cita
- **`appointment_id`**: ID único de la cita (índice único)
- **`patient_id`**: ID del paciente
- **`patient_document_number`**: Número de documento del paciente

###### Información del Paciente
- **`patient_full_name`**: Nombre completo del paciente
- **`patient_first_name`**: Primer nombre del paciente
- **`patient_last_name`**: Apellido del paciente
- **`patient_main_phone_number`**: Teléfono principal del paciente

###### Información de la Cita
- **`date_time_from`**: Fecha y hora de inicio de la cita
- **`duration`**: Duración de la cita en minutos
- **`status`**: Estado actual de la cita
- **`is_confirmed`**: Boolean que indica si la cita está confirmada
- **`appointment_type_id`**: Tipo de cita

###### Información del Centro Médico
- **`center_id`**: ID del centro médico
- **`center_name`**: Nombre del centro médico

###### Información del Servicio
- **`service_id`**: ID del servicio médico
- **`service_name`**: Nombre del servicio
- **`service_area_id`**: ID del área de servicio
- **`service_area_name`**: Nombre del área de servicio (ej: "medica", "dental")
- **`service_specialty_id`**: ID de la especialidad
- **`service_specialty_name`**: Nombre de la especialidad

###### Información del Doctor/Recurso
- **`resource_id`**: ID del doctor/recurso
- **`resource_name`**: Nombre del doctor/recurso

###### Información de Cobertura
- **`coverage_plan_id`**: ID del plan de cobertura
- **`coverage_plan_name`**: Nombre del plan de cobertura

###### Información de Campaña
- **`campaign_id`**: ID de la campaña
- **`template`**: Template utilizado

###### Metadatos
- **`created_on`**: Fecha de creación (string)
- **`created_at`**: Timestamp de creación
- **`updated_at`**: Timestamp de última actualización
- **`last_notification_date`**: Última fecha de notificación

### APIs y Integraciones
- **APIGEE**: API Gateway para RedSalud
- **WhatsApp Business API**: Canal de comunicación
- **requests**: 2.31.0 (Cliente HTTP)

### Utilidades
- **python-dotenv**: 1.0.0 (Variables de entorno)
- **PyYAML**: 6.0.1 (Parsing de YAML)
- **colorlog**: 6.7.0 (Logging con colores)
- **python-dateutil**: 2.8.2 (Manejo de fechas)

## Configuración del Entorno

### Variables de Entorno (.env)
```bash
# Configuración de Base de Datos PostgreSQL
DB_HOST=34.45.109.62
DB_USER=bot_client
DB_PORT=5432
DB_PASSWORD=Cg:m8mY=xZR?LB#*
DB_NAME=bot

# Configuración de APIGEE para RedSalud
APIGEE_API_URL=https://redsalud-qa.apigee.net
APIGEE_USERNAME=4tu0YPpudPmRE2bvgyheDbKnVAmPdCqK
APIGEE_PASSWORD=iHVNn0GZU0KJ2iN8
```

### Configuración de Rasa (config.yml)
```yaml
recipe: default.v1
language: es

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
    constrain_similarities: true
  - name: EntitySynonymMapper
  - name: ResponseSelector
    epochs: 100
    constrain_similarities: true
  - name: FallbackClassifier
    threshold: 0.7
    ambiguity_threshold: 0.1

policies:
  - name: MemoizationPolicy
  - name: RulePolicy
  - name: UnexpecTEDIntentPolicy
    max_history: 5
    epochs: 100
  - name: TEDPolicy
    max_history: 5
    epochs: 100
    constrain_similarities: true
```

## Estructura del Proyecto

### Archivos de Configuración
```
├── domain.yml              # Intents, entities, slots, responses
├── config.yml              # Pipeline NLU y políticas Core
├── credentials.yml         # Configuración WhatsApp
├── endpoints.yml           # Endpoints de Rasa
├── .env                    # Variables de entorno
└── requirements.txt        # Dependencias Python
```

### Datos de Entrenamiento
```
├── data/
│   ├── nlu.yml            # Ejemplos de intents
│   ├── stories.yml        # Flujos de conversación
│   └── rules.yml          # Reglas de comportamiento
```

### Código Fuente
```
├── actions/
│   ├── __init__.py        # Importaciones
│   ├── actions.py         # Acciones personalizadas
│   ├── database.py        # Conexión BD
│   └── utils.py           # Utilidades
├── logging_config.py      # Configuración logging
└── validate_setup.py      # Script de validación
```

## Intents y Entities

### Intents Principales
- `greet`: Saludos
- `affirm`: Confirmación (Sí)
- `deny`: Negación (No)
- `goodbye`: Despedidas
- `EXTERNAL_init_context`: Inicialización de contexto
- `EXTERNAL_init_rebooking`: Inicialización de rebooking
- `out_of_scope`: Texto aleatorio/sin sentido

### Entities (26 totales)
- `nombre_paciente`: Nombre del paciente
- `fecha_hora`: Fecha y hora de la cita
- `especialidad`: Especialidad médica
- `centro_medico`: Centro médico
- `resource_name`: Nombre del doctor
- `appointment_id`: ID de la cita
- `conversation_id`: ID de conversación
- `campaign_name`: Nombre de campaña
- Y 18 entidades adicionales...

### Slots Principales
- `contexto`: Contexto de la conversación ("confirmación" o "rebooking")
- `fecha_hora_formato`: Fecha formateada en español
- `operation_status`: Estado de operaciones (deprecated)

## Acciones Personalizadas

### Acciones Implementadas
1. **`ActionInitContext`**: Inicializa contexto con entidades
2. **`ActionInitRebooking`**: Inicializa contexto de rebooking
3. **`ActionFormatDate`**: Formatea fechas en español
4. **`ActionCancelAppointment`**: Cancela citas en RedSalud
5. **`ActionConfirmAppointment`**: Confirma citas en RedSalud
6. **`ActionFallback`**: Maneja mensajes no entendidos
7. **`ActionTestConnection`**: Prueba conexión a BD
8. **`ActionGetSystemStatus`**: Estado del sistema
9. **`ActionValidateInput`**: Valida entradas
10. **`ActionHandleError`**: Maneja errores

### Funciones de Base de Datos
1. **`update_appointment_status()`**: Actualiza estado de citas en BD
   - Parámetros: `appointment_id`, `status`
   - Actualiza: `status`, `last_notification_date`, `updated_at`
   - Estados: "confirmed", "confirmed error", "canceled", "canceled error"

### Funciones de API
1. **`obtener_access_token()`**: Obtiene token OAuth2
2. **`confirm_appointment()`**: Confirma cita en API
3. **`cancel_appointment()`**: Cancela cita en API

## Configuración de WhatsApp

### Credenciales (credentials.yml)
```yaml
rest:
  # Configuración para WhatsApp Business API
  # Los detalles específicos están en el archivo
```

### Respuestas Personalizadas
- **Templates de WhatsApp**: Para confirmaciones
- **Botones interactivos**: Para reconfirmaciones y rebooking
- **Mensajes de texto**: Para confirmaciones y errores

### Nuevas Respuestas de Rebooking
- **`utter_rebooking`**: Botones interactivos para reagendamiento
- **`utter_rebooking_confirmed`**: Confirmación de reagendamiento
- **`utter_rebooking_cancelled`**: Cancelación de reagendamiento
- **`utter_rebooking_ask_date`**: Solicita fecha y hora para reagendamiento

## Logging y Monitoreo

### Configuración de Logging
```python
# logging_config.py
LOG_LEVEL = "INFO"
LOG_FILE = "bot_confirmaciones.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Métricas Clave
- **Tasa de éxito de API**: Confirmaciones/cancelaciones/rebookings exitosas
- **Tiempo de respuesta**: Latencia de operaciones
- **Errores de autenticación**: Problemas con tokens
- **Uso de fallback**: Mensajes no entendidos

## Dependencias Críticas

### Core Dependencies
```
rasa==3.6.21
rasa-sdk==3.6.2
psycopg2-binary==2.9.7
python-dotenv==1.0.0
requests==2.31.0
PyYAML==6.0.1
colorlog==6.7.0
```

### Development Dependencies
```
pytest==7.4.3
pytest-asyncio==0.21.1
```

## Configuración de Desarrollo

### Entorno Virtual
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### Comandos Principales
```bash
rasa train                    # Entrenar modelo
rasa run actions             # Servidor de acciones
rasa shell                   # Chat interactivo
rasa test                    # Ejecutar tests
```

### Validación del Setup
```bash
python validate_setup.py     # Validar configuración
```

## Flujos de Conversación

### Flujo de Confirmación
1. **Inicialización**: `EXTERNAL_init_context` → `action_init_context`
2. **Contexto**: `contexto = "confirmación"`
3. **Saludo**: `greet` → `utter_greet` (template o botones)
4. **Respuesta**: `affirm` → `action_confirm_appointment` / `deny` → `action_cancel_appointment`

### Flujo de Rebooking
1. **Inicialización**: `EXTERNAL_init_rebooking` → `action_init_rebooking`
2. **Contexto**: `contexto = "rebooking"`
3. **Saludo**: `greet` → `utter_rebooking` (botones interactivos)
4. **Respuesta**: `affirm` → `utter_rebooking_confirmed` / `deny` → `utter_rebooking_cancelled`

### Flujo de Fallback
1. **Detección**: `nlu_fallback` o `out_of_scope`
2. **Acción**: `action_fallback`
3. **Respuesta**: Mensaje contextual según estado de la conversación

## Mejoras Implementadas

### Sistema de Fallback
- **Threshold aumentado**: De 0.3 a 0.7 para mayor precisión
- **Ejemplos de texto aleatorio**: 50+ ejemplos en `out_of_scope`
- **Fallback contextual**: Respuestas específicas según el contexto
- **Reglas mejoradas**: Manejo de `nlu_fallback` y `out_of_scope`

### Funcionalidad de Rebooking
- **Acción de inicialización**: `ActionInitRebooking`
- **Botones interactivos**: Para facilitar la interacción
- **Respuestas personalizadas**: Confirmación y cancelación específicas
- **Flujos completos**: Historias y reglas implementadas 