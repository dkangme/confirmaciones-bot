# Flujo de Rebooking Actualizado

## Resumen de Cambios

Se ha actualizado el flujo completo de rebooking para incorporar la acción `action_show_available_slots` después de `action_process_date_request`, reemplazando `utter_show_options` por una acción más dinámica que muestra los slots disponibles en tiempo real.

## Cambios Realizados

### 1. Historia de Rebooking (`data/rebooking_stories.yml`)

**Antes:**
```yaml
- story: complete rebooking flow
  steps:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  - intent: rebooking
  - action: utter_rebooking
  - intent: affirm
  - action: utter_rebooking_ask_date
  - intent: proponer_fecha
  - action: action_process_date_request
  - intent: seleccionar_opcion
  - action: action_process_slot_selection
  - intent: affirm_rebooking_confirm
  - action: action_confirm_rebooking
```

**Después:**
```yaml
- story: complete rebooking flow
  steps:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  - intent: rebooking
  - action: utter_rebooking
  - intent: affirm
  - action: utter_rebooking_ask_date
  - intent: proponer_fecha
  - action: action_process_date_request
  - action: action_show_available_slots  # ✅ NUEVA ACCIÓN
  - intent: seleccionar_opcion
  - action: action_process_slot_selection
  - intent: affirm_rebooking_confirm
  - action: action_confirm_rebooking
```

### 2. Reglas de Rebooking (`data/rules.yml`)

Se agregaron reglas completas para el flujo de rebooking:

```yaml
# ===== FLUJO DE REBOOKING =====

- rule: Initialize rebooking context when EXTERNAL_init_rebooking is triggered
  steps:
  - intent: EXTERNAL_init_rebooking
  - action: action_init_rebooking

- rule: Start rebooking flow when user confirms in rebooking context
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: rebooking
  - action: utter_rebooking

- rule: Ask for date when user affirms rebooking
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: affirm
  - action: utter_rebooking_ask_date

- rule: Process date request and show options
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: proponer_fecha
  - action: action_process_date_request
  - action: action_show_available_slots  # ✅ ACCIÓN DINÁMICA

- rule: Process slot selection
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: seleccionar_opcion
  - action: action_process_slot_selection

- rule: Confirm rebooking when user affirms
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: affirm_rebooking_confirm
  - action: action_confirm_rebooking

- rule: Cancel rebooking when user denies
  condition:
  - slot_was_set:
    - contexto_rebooking: "rebooking"
  steps:
  - intent: deny
  - action: action_cancel_rebooking
```

## Flujo Completo Actualizado

### 1. **Inicialización**
```
Usuario: [JSON con EXTERNAL_init_rebooking]
Bot: action_init_rebooking
```

### 2. **Confirmación de Rebooking**
```
Usuario: "Sí, quiero reagendar"
Bot: utter_rebooking
```

### 3. **Solicitud de Fecha**
```
Usuario: "Sí"
Bot: utter_rebooking_ask_date
```

### 4. **Procesamiento de Fecha**
```
Usuario: "mañana a las 10"
Bot: action_process_date_request
Bot: action_show_available_slots  # ✅ NUEVA ACCIÓN
```

### 5. **Selección de Horario**
```
Usuario: "1" (número de opción)
Bot: action_process_slot_selection
```

### 6. **Confirmación Final**
```
Usuario: "Sí, confirmo"
Bot: action_confirm_rebooking
```

## Diferencias Clave

### ✅ **action_show_available_slots vs utter_show_options**

| Aspecto | `utter_show_options` | `action_show_available_slots` |
|---------|---------------------|------------------------------|
| **Tipo** | Respuesta estática | Acción dinámica |
| **Contenido** | Opciones fijas | Slots reales de la API |
| **Flexibilidad** | Limitada | Alta |
| **Datos** | Hardcodeados | Dinámicos desde BD |
| **Formato** | Lista interactiva | Texto numerado |

### 🔧 **Funcionalidad de action_show_available_slots**

```python
def run(self, dispatcher, tracker, domain):
    # Obtener slots disponibles del slot
    available_slots = get_slot_value(tracker, "available_slots")
    
    if not available_slots:
        dispatcher.utter_message(text="❌ No hay horarios disponibles.")
        return []
    
    # Crear mensaje dinámico
    message = "📅 **Horarios disponibles:**\n\n"
    
    for i, slot in enumerate(available_slots, 1):
        message += f"{i}. {slot}\n"
    
    message += "\nResponde con el número de la opción que prefieras."
    
    dispatcher.utter_message(text=message)
```

## Beneficios del Cambio

### 🎯 **Mejor Experiencia de Usuario**
- Opciones reales y actualizadas
- Información dinámica basada en disponibilidad real
- Respuesta más rápida y precisa

### 🔄 **Flujo Más Robusto**
- Integración completa con la API de slots
- Manejo de errores mejorado
- Logs detallados para debugging

### 📊 **Datos Reales**
- Slots obtenidos de la API de RedSalud
- Disponibilidad en tiempo real
- Información actualizada

## Archivos Modificados

1. **`data/rebooking_stories.yml`**
   - ✅ Historia actualizada con `action_show_available_slots`

2. **`data/rules.yml`**
   - ✅ Reglas completas para el flujo de rebooking
   - ✅ Regla específica para mostrar opciones dinámicas

3. **`actions/rebooking_actions.py`**
   - ✅ Acción `ActionShowAvailableSlots` implementada
   - ✅ Logs detallados para debugging

## Testing del Flujo

### Comandos para Probar

```bash
# Entrenar el modelo con los cambios
rasa train

# Probar el flujo completo
rasa shell

# Verificar las reglas
rasa test core
```

### Ejemplo de Conversación

```
Usuario: [JSON con datos de rebooking]
Bot: ✅ Contexto de Rebooking Inicializado

Usuario: "Sí, quiero reagendar"
Bot: 🔄 Perfecto, vamos a buscar una nueva fecha...

Usuario: "Sí"
Bot: Por favor, indícame qué fecha y hora te gustaría...

Usuario: "mañana a las 10"
Bot: Perfecto, entiendo que quieres reagendar para el **mañana a las 10**...
Bot: 📅 **Horarios disponibles:**
     1. lunes 15 de julio de 2024 a las 09:00
     2. lunes 15 de julio de 2024 a las 09:15
     3. lunes 15 de julio de 2024 a las 09:30
     Responde con el número de la opción que prefieras.

Usuario: "1"
Bot: ✅ Perfecto, has seleccionado: **lunes 15 de julio de 2024 a las 09:00**
     ¿Confirmas que quieres reagendar tu cita para este horario?

Usuario: "Sí, confirmo"
Bot: ✅ ¡Reagendamiento confirmado!
```

## Notas Técnicas

- **Compatibilidad**: El flujo es compatible con el sistema existente
- **Logs**: Se mantienen los logs detallados implementados anteriormente
- **Error Handling**: Manejo robusto de errores en cada paso
- **Performance**: Acciones optimizadas para respuesta rápida 