# Active Context: Bot de Confirmaciones RedSalud

## Estado Actual del Proyecto

### ✅ Funcionalidades Completadas
1. **Configuración Base**: Proyecto Rasa configurado con todas las dependencias
2. **Integración API**: Conexión con RedSalud/Apigee para confirmar/cancelar citas
3. **Manejo de Contexto**: Intent `EXTERNAL_init_context` para inicializar slots
4. **Flujos de Conversación**: Confirmación y cancelación de citas
5. **Formateo de Fechas**: Fechas en formato español legible
6. **Sistema de Fallback**: Manejo de mensajes no entendidos
7. **Variables de Entorno**: Configuración completa de credenciales
8. **Logging**: Sistema de logs configurado con PostgreSQL
9. **Funcionalidad de Rebooking**: Sistema completo de reagendamiento de citas
10. **Documentación de BD**: Esquema de tabla `appointments` documentado en memory bank
11. **Actualización de Estados**: Función para actualizar estados de citas en BD
12. **Sistema de Slots Optimizados**: Función `get_slots_optimized` implementada
13. **Procesamiento de Fechas**: Acción `ActionProcessDateRequest` para extraer fechas del usuario
14. **Corrección de Parámetros**: Todos los parámetros de `get_slots_optimized` corregidos

### 🔄 Trabajo en Progreso
- **Memory Bank**: Documentación completa del proyecto (EN PROGRESO)
- **Validación**: Verificación de configuración y dependencias
- **Testing**: Pruebas de integración con API de RedSalud

### 📋 Próximos Pasos Inmediatos
1. **Entrenar Modelo**: Ejecutar `rasa train` con configuración actual
2. **Probar Fallback**: Verificar funcionamiento del sistema de fallback
3. **Validar API**: Probar conexión con RedSalud/Apigee
4. **Probar Rebooking**: Validar flujo completo de reagendamiento
5. **Optimizar Respuestas**: Revisar y mejorar mensajes de WhatsApp

## Decisiones Técnicas Activas

### 1. **Configuración de Fallback**
- **Decisión**: Usar `ActionFallback` personalizado en lugar del fallback por defecto
- **Razón**: Mayor control sobre respuestas y experiencia de usuario
- **Estado**: ✅ Implementado y configurado

### 2. **Manejo de Errores**
- **Decisión**: Acciones manejan errores directamente en lugar de usar slots
- **Razón**: Simplifica el flujo y reduce complejidad
- **Estado**: ✅ Implementado

### 3. **Formato de Fechas**
- **Decisión**: Formato español verbose ("miércoles 2 de julio de 2025 a las 13:30")
- **Razón**: Mejor experiencia de usuario en español
- **Estado**: ✅ Implementado

### 4. **Variables de Entorno**
- **Decisión**: Usar APIGEE_* para credenciales de RedSalud
- **Razón**: Separación clara entre configuraciones
- **Estado**: ✅ Configurado

### 5. **Funcionalidad de Rebooking**
- **Decisión**: Implementar flujo completo de reagendamiento con botones interactivos
- **Razón**: Mejorar experiencia de usuario para cambios de cita
- **Estado**: ✅ Implementado

### 6. **Separación de Funcionalidad de Rebooking**
- **Decisión**: Separar lógica de rebooking en archivos propios para mejor organización
- **Razón**: Mejorar mantenibilidad y escalabilidad del código
- **Estado**: ✅ Implementado (archivos separados creados)

### 7. **Actualización de Estados de Citas**
- **Decisión**: Implementar función para actualizar estados de citas en base de datos
- **Razón**: Mantener sincronización entre API y BD, tracking de operaciones
- **Estado**: ✅ Implementado (función update_appointment_status creada)

### 8. **Corrección de Mapeo de Slots**
- **Decisión**: Usar `conversation_id` como `appointment_id` en acciones de confirmación y cancelación
- **Razón**: Alinear con la estructura de datos real del sistema
- **Estado**: ✅ Implementado (código y documentación actualizados)

### 9. **Sistema de Slots Optimizados**
- **Decisión**: Implementar función `get_slots_optimized` para obtener horarios disponibles
- **Razón**: Permitir reagendamiento con horarios reales del sistema
- **Estado**: ✅ Implementado con parámetros corregidos

### 10. **Corrección de Parámetros de API**
- **Decisión**: Corregir todos los parámetros de `get_slots_optimized` para usar slots correctos
- **Razón**: Asegurar que los valores se obtengan de los slots apropiados
- **Estado**: ✅ Implementado (resource_id, patient_id, finish_time corregidos)

## Problemas Resueltos Recientemente

### 1. **Error de Credenciales APIGEE**
- **Problema**: "Faltan credenciales: auth_url, client_id, client_secret"
- **Solución**: Cambiar nombres de variables de entorno a APIGEE_*
- **Estado**: ✅ Resuelto

### 2. **Error de Sintaxis YAML**
- **Problema**: Indentación incorrecta en config.yml
- **Solución**: Corregir indentación de pipeline y policies
- **Estado**: ✅ Resuelto

### 3. **Dependencias Faltantes**
- **Problema**: `colorlog` y `PyYAML` no instalados
- **Solución**: Instalar dependencias faltantes
- **Estado**: ✅ Resuelto

### 4. **FallbackPolicy Deprecada**
- **Problema**: `FallbackPolicy` no válida en Rasa 3.x
- **Solución**: Eliminar política y usar solo `FallbackClassifier` + reglas
- **Estado**: ✅ Resuelto

### 5. **Sistema de Fallback Mejorado**
- **Problema**: Fallback no se activaba correctamente
- **Solución**: Aumentar threshold a 0.7 y añadir ejemplos de texto aleatorio
- **Estado**: ✅ Resuelto

### 6. **Slots Faltantes en Domain**
- **Problema**: Errores de slots no existentes en domain.yml
- **Solución**: Agregar todos los slots faltantes al domain.yml
- **Estado**: ✅ Resuelto

### 7. **Parámetros Incorrectos en get_slots_optimized**
- **Problema**: `patient_id` obtenido de `phone_number` en lugar de `patient_id`
- **Solución**: Corregir para usar el slot correcto `patient_id`
- **Estado**: ✅ Resuelto

### 8. **Parámetro finish_time vs end_time**
- **Problema**: Confusión entre `finish_time` y `end_time` en llamadas a API
- **Solución**: Usar `end_time` como parámetro y `finish_time` en la llamada a la función
- **Estado**: ✅ Resuelto

### 9. **Resource ID Mapping**
- **Problema**: `resource_id` obtenido de `resource_name` incorrectamente
- **Solución**: Usar `resource_id` con fallback a `resource_name`
- **Estado**: ✅ Resuelto

## Configuración Actual

### Archivos Críticos
- **config.yml**: Pipeline NLU y políticas configuradas (threshold fallback: 0.7)
- **domain.yml**: 26 entidades, slots y respuestas definidas (incluye rebooking)
- **actions/actions.py**: 10 acciones personalizadas implementadas
- **actions/rebooking_actions.py**: Acciones específicas de rebooking implementadas
- **.env**: Variables de entorno para BD y APIGEE

### Nuevas Funcionalidades
- **ActionInitRebooking**: Inicializa contexto de reagendamiento
- **ActionProcessDateRequest**: Procesa expresiones de fecha/hora del usuario
- **ActionShowAvailableSlots**: Muestra horarios disponibles
- **ActionProcessSlotSelection**: Procesa selección de horario
- **ActionConfirmRebooking**: Confirma reagendamiento
- **ActionCancelRebooking**: Cancela reagendamiento
- **get_slots_optimized**: Función para obtener horarios disponibles
- **process_available_slots**: Procesa respuesta de slots disponibles

### Slots de Rebooking
- **rebooking_fecha**: Fecha extraída del usuario
- **rebooking_hora**: Hora extraída del usuario
- **start_time**: Tiempo de inicio en formato ISO
- **end_time**: Tiempo de fin en formato ISO
- **available_slots**: Lista de horarios disponibles
- **selected_slot**: Horario seleccionado por el usuario
- **slot_selection_index**: Índice de la selección

### Endpoints Configurados
- **Action Server**: Puerto 5055
- **API Server**: Puerto 5005
- **WhatsApp**: Configurado en credentials.yml

## Métricas de Rendimiento

### Configuración de Modelo
- **Epochs**: 100 para DIETClassifier y ResponseSelector
- **Threshold**: 0.7 para fallback (mejorado)
- **Language**: Español (es)

### Timeouts
- **API RedSalud**: 90 segundos
- **Token Cache**: Implementado para eficiencia

## Próximas Iteraciones

### Fase 1: Validación (Inmediata)
1. Entrenar modelo con configuración actual
2. Probar flujos de confirmación/cancelación
3. Probar flujo completo de rebooking
4. Validar integración con API de RedSalud
5. Verificar funcionamiento del fallback

### Fase 2: Optimización (Corto Plazo)
1. Mejorar respuestas de WhatsApp
2. Optimizar manejo de errores
3. Añadir más ejemplos de entrenamiento
4. Implementar métricas de rendimiento

### Fase 3: Escalabilidad (Mediano Plazo)
1. Implementar cache de tokens más robusto
2. Añadir monitoreo avanzado
3. Optimizar consultas de base de datos
4. Implementar rate limiting

## Notas de Desarrollo

### Comandos Útiles
```bash
# Entrenar modelo
rasa train

# Ejecutar servidor de acciones
rasa run actions

# Probar chat interactivo
rasa shell

# Validar configuración
python validate_setup.py
```

### Archivos de Log
- **bot_confirmaciones.log**: Logs principales del bot
- **PostgreSQL**: Logs de operaciones de BD

### Debugging
- **Log Level**: INFO configurado
- **Error Tracking**: Implementado en todas las acciones
- **API Response Logging**: Habilitado para debugging

### Nuevos Flujos de Conversación
1. **Confirmación**: `EXTERNAL_init_context` → `greet` → `affirm/deny`
2. **Reagendamiento**: `EXTERNAL_init_rebooking` → `greet` → `affirm/deny`
3. **Procesamiento de Fecha**: `proponer_fecha` → `action_process_date_request`
4. **Selección de Horario**: `seleccionar_opcion` → `action_process_slot_selection`
5. **Confirmación de Rebooking**: `affirm_rebooking_confirm` → `action_confirm_rebooking`
6. **Fallback**: `nlu_fallback` o `out_of_scope` → `action_fallback` 