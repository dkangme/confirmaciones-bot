# Project Brief: Bot de Confirmaciones RedSalud

## Proyecto
**Nombre**: Bot de Confirmaciones para RedSalud  
**Versión**: 3.6.21  
**Tipo**: Chatbot de confirmación de citas médicas  
**Plataforma**: WhatsApp Business API  

## Objetivo Principal
Automatizar el proceso de confirmación y cancelación de citas médicas en RedSalud, proporcionando una experiencia de usuario fluida y eficiente a través de WhatsApp.

## Alcance del Proyecto

### Funcionalidades Core
1. **Inicialización de Contexto**: Recibir y procesar información de citas médicas
2. **Confirmación de Citas**: Confirmar citas en la API de RedSalud/Apigee
3. **Cancelación de Citas**: Cancelar citas con manejo de errores
4. **Formateo de Fechas**: Presentar fechas en formato español legible
5. **Fallback**: Manejar mensajes no entendidos con respuestas útiles

### Integraciones
- **API RedSalud/Apigee**: Para confirmar y cancelar citas
- **PostgreSQL**: Base de datos para logging y auditoría
- **WhatsApp Business API**: Canal de comunicación principal

## Tecnologías
- **Rasa**: 3.6.21 (Framework de chatbot)
- **Python**: 3.8.10
- **PostgreSQL**: Base de datos
- **APIGEE**: API Gateway para RedSalud
- **WhatsApp Business API**: Canal de comunicación

## Entorno de Desarrollo
- **OS**: macOS (darwin 24.5.0)
- **Shell**: /bin/zsh
- **Directorio**: /Volumes/Kangme/2025/Proyectos/2Brains/red-salud/bot-confirmaciones

## Estado Actual
✅ **Completado**:
- Configuración base del proyecto
- Integración con API de RedSalud/Apigee
- Sistema de confirmación y cancelación de citas
- Manejo de errores y fallback
- Formateo de fechas en español
- Variables de entorno configuradas

🔄 **En Desarrollo**:
- Pruebas de integración
- Optimización de respuestas

## Próximos Pasos
1. Entrenar modelo con configuración actual
2. Probar flujos de confirmación y cancelación
3. Validar integración con API de RedSalud
4. Optimizar respuestas y manejo de errores 