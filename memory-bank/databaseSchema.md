# Database Schema: Bot de Confirmaciones RedSalud

## Tabla `appointments`

### Estructura Completa
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

## Análisis de Campos

### Campos de Identificación
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `id` | UUID | Clave primaria | No usado directamente |
| `appointment_id` | VARCHAR | ID único de la cita | Slot `conversation_id` |
| `patient_id` | VARCHAR | ID del paciente | Slot `patient_id` |
| `patient_document_number` | VARCHAR | Número de documento | No usado actualmente |

### Información del Paciente
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `patient_full_name` | VARCHAR | Nombre completo | Slot `nombre_paciente` |
| `patient_first_name` | VARCHAR | Primer nombre | No usado actualmente |
| `patient_last_name` | VARCHAR | Apellido | No usado actualmente |
| `patient_main_phone_number` | VARCHAR | Teléfono principal | Slot `patient_phone` |

### Información de la Cita
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `date_time_from` | VARCHAR | Fecha y hora de inicio | Slot `fecha_hora` |
| `duration` | INTEGER | Duración en minutos | Slot `duration` |
| `status` | VARCHAR | Estado de la cita | Slot `status` |
| `is_confirmed` | BOOLEAN | Si está confirmada | Slot `is_confirmed` |
| `appointment_type_id` | VARCHAR | Tipo de cita | No usado actualmente |

### Información del Centro Médico
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `center_id` | VARCHAR | ID del centro | No usado actualmente |
| `center_name` | VARCHAR | Nombre del centro | Slot `centro_medico` |

### Información del Servicio
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `service_id` | VARCHAR | ID del servicio | No usado actualmente |
| `service_name` | VARCHAR | Nombre del servicio | Slot `service_name` |
| `service_area_id` | VARCHAR | ID del área | No usado actualmente |
| `service_area_name` | VARCHAR | Nombre del área | Slot `area_medica` |
| `service_specialty_id` | VARCHAR | ID de especialidad | No usado actualmente |
| `service_specialty_name` | VARCHAR | Nombre de especialidad | Slot `especialidad` |

### Información del Doctor/Recurso
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `resource_id` | VARCHAR | ID del doctor | No usado actualmente |
| `resource_name` | VARCHAR | Nombre del doctor | Slot `resource_name` |

### Información de Cobertura
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `coverage_plan_id` | VARCHAR | ID del plan | No usado actualmente |
| `coverage_plan_name` | VARCHAR | Nombre del plan | Slot `coverage_plan` |

### Información de Campaña
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `campaign_id` | VARCHAR | ID de la campaña | Slot `conversation_id` |
| `template` | VARCHAR | Template utilizado | No usado actualmente |

### Metadatos
| Campo | Tipo | Descripción | Uso en Bot |
|-------|------|-------------|------------|
| `created_on` | VARCHAR | Fecha de creación | No usado actualmente |
| `created_at` | TIMESTAMP | Timestamp de creación | No usado actualmente |
| `updated_at` | TIMESTAMP | Timestamp de actualización | No usado actualmente |
| `last_notification_date` | TIMESTAMP | Última notificación | No usado actualmente |

## Relación con el Bot

### Slots Mapeados
El bot utiliza los siguientes campos de la tabla `appointments`:

1. **`appointment_id`** → Slot `conversation_id`
   - Usado para operaciones API (confirmar/cancelar)
   - Identificador único de la cita
   - **IMPORTANTE**: El appointment_id se obtiene del slot conversation_id

2. **`patient_full_name`** → Slot `nombre_paciente`
   - Mostrado en mensajes al usuario
   - Personalización de respuestas

3. **`resource_name`** → Slot `resource_name`
   - Nombre del doctor
   - Incluido en mensajes de confirmación

4. **`center_name`** → Slot `centro_medico`
   - Nombre del centro médico
   - Información de ubicación

5. **`date_time_from`** → Slot `fecha_hora`
   - Fecha y hora de la cita
   - Formateado para mostrar al usuario

6. **`service_specialty_name`** → Slot `especialidad`
   - Especialidad médica
   - Usado para lógica condicional

7. **`service_area_name`** → Slot `area_medica`
   - Área de servicio (medica/dental)
   - Determina tipo de mensaje

8. **`campaign_id`** → Slot `conversation_id`
   - ID de la campaña/conversación
   - Tracking de conversaciones
   - **NOTA**: Este campo también se usa como appointment_id

### Campos No Utilizados
Los siguientes campos están disponibles pero no se usan actualmente:
- `patient_first_name`, `patient_last_name`
- `patient_document_number`
- `center_id`, `service_id`
- `service_area_id`, `service_specialty_id`
- `resource_id`, `coverage_plan_id`
- `appointment_type_id`
- `template`
- Todos los campos de metadatos

### Estados de Citas
El campo `status` puede tener los siguientes valores:
- **"confirmed"**: Cita confirmada exitosamente
- **"confirmed error"**: Error al confirmar la cita
- **"canceled"**: Cita cancelada exitosamente
- **"canceled error"**: Error al cancelar la cita
- **Otros estados**: Definidos por el sistema principal

## Operaciones de Base de Datos

### Conexión
```python
# actions/database.py
def db_connection():
    """Establece conexión con PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
```

### Consultas Típicas
```sql
-- Obtener cita por appointment_id
SELECT * FROM appointments WHERE appointment_id = %s;

-- Actualizar estado de confirmación
UPDATE appointments 
SET is_confirmed = true, updated_at = now() 
WHERE appointment_id = %s;

-- Obtener citas pendientes de confirmación
SELECT * FROM appointments 
WHERE is_confirmed = false 
AND status = 'active';

-- Actualizar estado de cita (nueva función)
UPDATE appointments 
SET status = %s, 
    last_notification_date = NOW(), 
    updated_at = NOW()
WHERE appointment_id = %s;

-- Obtener citas por estado
SELECT * FROM appointments WHERE status = 'confirmed';
SELECT * FROM appointments WHERE status = 'canceled';
SELECT * FROM appointments WHERE status LIKE '%error%';
```

## Consideraciones de Diseño

### Índices
- **Primario**: `id` (UUID)
- **Único**: `appointment_id` (para búsquedas rápidas)

### Constraints
- **NOT NULL**: `id`, `appointment_id`, `created_at`, `updated_at`
- **DEFAULT**: `is_confirmed = false`, timestamps automáticos

### Tipos de Datos
- **VARCHAR**: Para IDs y nombres (flexibilidad)
- **TIMESTAMP**: Para fechas de auditoría
- **BOOLEAN**: Para flags simples
- **INTEGER**: Para duración

## Posibles Mejoras

### Campos Adicionales
- `confirmation_date`: Fecha de confirmación
- `cancellation_date`: Fecha de cancelación
- `confirmation_method`: Método de confirmación (bot, manual, etc.)
- `user_id`: ID del usuario que confirmó/canceló

### Índices Adicionales
- `idx_appointments_patient_id`: Para búsquedas por paciente
- `idx_appointments_status`: Para filtros por estado
- `idx_appointments_date_time`: Para consultas por fecha

### Optimizaciones
- Particionamiento por fecha
- Archivo de datos históricos
- Cache de consultas frecuentes 