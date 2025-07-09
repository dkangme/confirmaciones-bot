# Mensaje de Commit

```
feat: actualizar flujo de rebooking con action_show_available_slots y corregir reglas contradictorias

## Cambios Principales

### 🔄 Flujo de Rebooking Actualizado
- Incorporar action_show_available_slots después de action_process_date_request
- Reemplazar utter_show_options por acción dinámica que muestra slots reales
- Mejorar experiencia de usuario con datos actualizados de la API

### 🛠️ Corrección de Reglas Contradictorias
- Eliminar reglas duplicadas entre rules.yml y rebooking_rules.yml
- Consolidar todas las reglas de rebooking en data/rules.yml
- Corregir regla "Handle date proposal" para incluir action_show_available_slots

## Archivos Modificados

### data/rebooking_stories.yml
- Actualizar historia "complete rebooking flow"
- Agregar action_show_available_slots en secuencia correcta

### data/rules.yml
- Eliminar reglas duplicadas de rebooking
- Agregar reglas unificadas para todo el flujo de rebooking
- Incluir reglas de fallback específicas para contexto rebooking

### data/rebooking_rules.yml
- Actualizar regla "Handle date proposal" con action_show_available_slots
- Mantener consistencia con reglas principales

## Beneficios

### 🎯 Mejor Experiencia de Usuario
- Opciones dinámicas basadas en disponibilidad real
- Información actualizada desde la API de RedSalud
- Respuestas más precisas y relevantes

### 🔧 Flujo Más Robusto
- Integración completa con API de slots
- Manejo de errores mejorado
- Logs detallados para debugging

### 📊 Datos Reales
- Slots obtenidos de la API de RedSalud
- Disponibilidad en tiempo real
- Información actualizada

## Testing

### Comandos de Verificación
```bash
rasa train          # Entrenar modelo sin errores
rasa test core      # Verificar reglas sin contradicciones
rasa shell          # Probar flujo completo
```

### Flujo Actualizado
1. EXTERNAL_init_rebooking → action_init_rebooking
2. rebooking → utter_rebooking
3. affirm → utter_rebooking_ask_date
4. proponer_fecha → action_process_date_request → action_show_available_slots
5. seleccionar_opcion → action_process_slot_selection
6. affirm_rebooking_confirm → action_confirm_rebooking

## Documentación

### Archivos Creados
- FLUJO_REBOOKING_ACTUALIZADO.md: Documentación del flujo actualizado
- CORRECCION_REGLAS_REBOOKING.md: Explicación de la corrección de reglas

## Notas Técnicas

- Compatibilidad: Mantiene funcionalidad original
- Performance: Eliminación de reglas duplicadas mejora rendimiento
- Mantenimiento: Un solo archivo para todas las reglas
- Logs: Mantiene logging detallado implementado anteriormente

## Breaking Changes
- Ninguno: Cambios son compatibles hacia atrás
- Reglas existentes mantienen funcionalidad
- Flujo de confirmación no afectado

## Dependencias
- Requiere action_show_available_slots implementada en actions/rebooking_actions.py
- Compatible con logging mejorado implementado anteriormente
- Funciona con API de RedSalud configurada
```

## Versión Corta para Git

```
feat: actualizar flujo rebooking con action_show_available_slots y corregir reglas contradictorias

- Incorporar action_show_available_slots después de action_process_date_request
- Eliminar reglas duplicadas entre rules.yml y rebooking_rules.yml
- Consolidar reglas de rebooking en data/rules.yml
- Mejorar UX con slots dinámicos de la API
- Corregir regla "Handle date proposal" para incluir action_show_available_slots

Archivos: data/rebooking_stories.yml, data/rules.yml, data/rebooking_rules.yml
Docs: FLUJO_REBOOKING_ACTUALIZADO.md, CORRECCION_REGLAS_REBOOKING.md
``` 