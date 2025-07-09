# Logs Mejorados para get_slots_optimized

## Resumen de Mejoras

Se han implementado logs detallados y estructurados para la función `get_slots_optimized` que proporcionan información completa sobre:

- ✅ **Respuestas exitosas** con detalles completos
- ✅ **Errores detallados** con contexto completo
- ✅ **Estadísticas de slots** disponibles y no disponibles
- ✅ **Información de rendimiento** (tiempo de respuesta)
- ✅ **Estructura de datos** de la respuesta

## Estructura de los Logs

### 1. Logs de Respuesta Exitosa

```
✅ RESPUESTA EXITOSA DE get_slots_optimized:
   Status Code: 200
   Content-Type: application/json
   Content-Length: 2048

📊 ESTRUCTURA DE LA RESPUESTA:
   Claves principales: ['slots', 'count', 'metadata']
   Número total de slots: 15
   Slots disponibles: 8
   Slots no disponibles: 7

📅 DETALLES DE SLOTS (primeros 5):
   Slot 1:
     - Timestamp: 1734567890 (2024-12-20 10:30:00)
     - Bookable: True
     - StartTime: 2024-12-20T10:30:00-04:00
     - EndTime: 2024-12-20T10:45:00-04:00
     - ResourceId: 7dbd3ae4-4ead-4fcf-a131-a5fa005e35a5
   Slot 2:
     - Timestamp: 1734567900 (2024-12-20 10:45:00)
     - Bookable: False
     - StartTime: 2024-12-20T10:45:00-04:00
     - EndTime: 2024-12-20T11:00:00-04:00
     - ResourceId: 7dbd3ae4-4ead-4fcf-a131-a5fa005e35a5
   ...

📈 ESTADÍSTICAS DE SLOTS DISPONIBLES:
     - Fechas únicas disponibles: 3
     - Fechas: ['2024-12-20', '2024-12-21', '2024-12-22']

🎉 get_slots_optimized completado exitosamente
   URL llamada: https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized(...)
   Tiempo de respuesta: 1.23s
```

### 2. Logs de Error Detallados

```
❌ ERROR en get_slots_optimized:
   Tipo de error: HTTPError
   Mensaje: 404 Client Error: Not Found for url: https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized(...)
   URL que falló: https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized(...)
   Status Code: 404
   Response Headers: {'content-type': 'application/json', 'server': 'nginx', ...}
   Response Text: {"error": "Resource not found", "code": "RESOURCE_NOT_FOUND"}
```

### 3. Logs de Error de Conexión

```
❌ ERROR en get_slots_optimized:
   Tipo de error: ConnectionError
   Mensaje: Failed to establish a new connection: [Errno 110] Connection timed out
   URL que falló: https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized(...)
   Sin respuesta del servidor (error de conexión)
```

## Información Capturada

### Para Respuestas Exitosas

1. **Información de HTTP**:
   - Status Code
   - Content-Type
   - Content-Length

2. **Estructura de Datos**:
   - Claves principales de la respuesta
   - Número total de slots
   - Conteo de slots disponibles vs no disponibles

3. **Detalles de Slots**:
   - Timestamp (con conversión a fecha legible)
   - Estado de disponibilidad (Bookable)
   - Horarios de inicio y fin
   - ID del recurso

4. **Estadísticas**:
   - Fechas únicas disponibles
   - Distribución temporal de slots

5. **Información de Rendimiento**:
   - URL completa llamada
   - Tiempo de respuesta

### Para Errores

1. **Tipo de Error**:
   - Nombre de la excepción
   - Mensaje de error
   - URL que falló

2. **Detalles de Respuesta** (si aplica):
   - Status Code
   - Headers de respuesta
   - Texto de respuesta

3. **Contexto de Conexión**:
   - Indicación si es error de conexión
   - Información de red

## Beneficios de los Logs Mejorados

### 🔍 **Debugging Mejorado**
- Información completa para diagnosticar problemas
- Contexto detallado de errores
- Trazabilidad completa de llamadas

### 📊 **Monitoreo de Rendimiento**
- Tiempo de respuesta de cada llamada
- Estadísticas de disponibilidad
- Métricas de uso

### 🛠️ **Mantenimiento**
- Logs estructurados fáciles de parsear
- Información consistente en todos los casos
- Separación clara entre éxito y error

### 📈 **Análisis de Datos**
- Estadísticas de slots disponibles
- Distribución temporal de horarios
- Patrones de uso de la API

## Uso de los Logs

### Para Desarrollo
```bash
# Ver logs en tiempo real
tail -f bot_confirmaciones.log | grep "get_slots_optimized"

# Buscar errores específicos
grep "ERROR en get_slots_optimized" bot_confirmaciones.log

# Buscar respuestas exitosas
grep "RESPUESTA EXITOSA DE get_slots_optimized" bot_confirmaciones.log
```

### Para Monitoreo
```bash
# Contar llamadas exitosas
grep -c "get_slots_optimized completado exitosamente" bot_confirmaciones.log

# Contar errores
grep -c "ERROR en get_slots_optimized" bot_confirmaciones.log

# Ver tiempo promedio de respuesta
grep "Tiempo de respuesta" bot_confirmaciones.log | awk '{print $NF}' | awk '{sum+=$1; count++} END {print "Promedio:", sum/count "s"}'
```

## Archivos Relacionados

- `actions/rebooking_actions.py`: Función con logs mejorados
- `test_logging_slots.py`: Script de prueba para logs
- `LOGS_MEJORADOS.md`: Este documento
- `bot_confirmaciones.log`: Archivo de logs principal

## Configuración de Logging

Los logs utilizan la configuración estándar del proyecto:

```python
import logging
logger = logging.getLogger(__name__)

# Los logs se escriben en:
# - bot_confirmaciones.log (archivo principal)
# - stdout (consola durante desarrollo)
```

## Notas Técnicas

- **Formato**: Logs estructurados con emojis para fácil identificación
- **Nivel**: INFO para respuestas exitosas, ERROR para errores
- **Rendimiento**: Logs optimizados para no impactar el rendimiento
- **Privacidad**: Tokens de autorización ocultos en logs
- **Rotación**: Los logs se rotan automáticamente por el sistema 