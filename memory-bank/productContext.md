# Product Context: Bot de Confirmaciones RedSalud

## Propósito del Producto

### Objetivo Principal
El Bot de Confirmaciones RedSalud es un chatbot inteligente diseñado para automatizar y mejorar el proceso de confirmación y gestión de citas médicas en la red de salud. El bot facilita la comunicación con pacientes a través de WhatsApp, reduciendo la carga administrativa y mejorando la experiencia del usuario.

### Problemas que Resuelve
1. **Carga Administrativa**: Reduce el trabajo manual de confirmación de citas
2. **Comunicación Eficiente**: Proporciona respuestas inmediatas a pacientes
3. **Gestión de Citas**: Permite confirmar, cancelar y reagendar citas fácilmente
4. **Experiencia del Paciente**: Ofrece una interfaz conversacional natural
5. **Integración de Sistemas**: Conecta WhatsApp con el sistema de citas de RedSalud

## Funcionalidades del Producto

### 1. **Confirmación de Citas** ✅
- **Descripción**: Permite a los pacientes confirmar sus citas médicas
- **Flujo**: 
  1. Inicialización con datos de la cita
  2. Saludo personalizado con información de la cita
  3. Opción de confirmar o cancelar
  4. Integración con API de RedSalud para actualizar estado
- **Beneficios**: Reduce no-shows y mejora la planificación médica

### 2. **Cancelación de Citas** ✅
- **Descripción**: Permite a los pacientes cancelar citas cuando sea necesario
- **Flujo**:
  1. Mismo flujo inicial que confirmación
  2. Opción de cancelar con razón específica
  3. Actualización en sistema de RedSalud
- **Beneficios**: Libera slots para otros pacientes y mejora la eficiencia

### 3. **Reagendamiento de Citas** ✅
- **Descripción**: Permite a los pacientes reagendar sus citas médicas
- **Flujo**:
  1. Inicialización específica para rebooking
  2. Botones interactivos para facilitar la decisión
  3. Confirmación o cancelación del reagendamiento
  4. Respuestas específicas para cada caso
- **Beneficios**: Mejora la satisfacción del paciente y reduce cancelaciones

### 4. **Sistema de Fallback Inteligente** ✅
- **Descripción**: Maneja mensajes no entendidos de forma contextual
- **Características**:
  - Threshold configurado en 0.7 para mayor precisión
  - Respuestas específicas según el contexto de la conversación
  - Opciones útiles para guiar al usuario
- **Beneficios**: Mejora la experiencia del usuario y reduce frustración

### 5. **Integración con WhatsApp** ✅
- **Descripción**: Comunicación nativa a través de WhatsApp Business API
- **Características**:
  - Templates personalizados para diferentes tipos de confirmación
  - Botones interactivos para facilitar la interacción
  - Formato de fechas en español legible
  - Mensajes de error y éxito claros
- **Beneficios**: Canal de comunicación familiar y accesible

## Experiencia del Usuario

### Flujo de Usuario Típico

#### Confirmación de Cita
```
1. Usuario recibe mensaje de WhatsApp
2. Bot presenta información de la cita de forma clara
3. Usuario puede confirmar o cancelar fácilmente
4. Bot confirma la acción y proporciona detalles
5. Sistema se actualiza automáticamente
```

#### Reagendamiento de Cita
```
1. Usuario recibe mensaje de WhatsApp para reagendamiento
2. Bot presenta opciones con botones interactivos
3. Usuario puede confirmar o cancelar el reagendamiento
4. Bot proporciona confirmación específica
5. Proceso se completa sin intervención manual
```

### Características de UX

#### Mensajes Personalizados
- **Información Contextual**: Fecha, hora, doctor, especialidad, centro médico
- **Formato Legible**: Fechas en español ("miércoles 2 de julio de 2025 a las 13:30")
- **Tono Amigable**: Comunicación clara y profesional

#### Interfaz Conversacional
- **Botones Interactivos**: Para facilitar respuestas rápidas
- **Opciones Claras**: Sí/No para decisiones simples
- **Feedback Inmediato**: Confirmación de acciones realizadas

#### Manejo de Errores
- **Mensajes Claros**: Explicación de problemas cuando ocurren
- **Opciones Alternativas**: Guía para resolver problemas
- **Soporte Contextual**: Ayuda específica según la situación

## Integración con Sistemas

### API de RedSalud
- **Autenticación**: OAuth2 a través de APIGEE
- **Endpoints**:
  - Confirmación: `/agendarsv2/cita/confirmar/`
  - Cancelación: `/agendarsv2/cita/anular/`
- **Manejo de Errores**: Timeouts y reintentos automáticos

### Base de Datos PostgreSQL
- **Logging**: Registro de todas las operaciones
- **Métricas**: Seguimiento de éxito/fallo de operaciones
- **Auditoría**: Trazabilidad completa de conversaciones

### WhatsApp Business API
- **Templates**: Mensajes pre-aprobados para confirmaciones
- **Botones**: Interacciones rápidas para decisiones
- **Formato**: Texto y elementos interactivos

## Métricas de Éxito

### KPIs del Producto
1. **Tasa de Confirmación**: Porcentaje de citas confirmadas exitosamente
2. **Tasa de Cancelación**: Porcentaje de cancelaciones procesadas
3. **Tasa de Rebooking**: Porcentaje de reagendamientos exitosos
4. **Tiempo de Respuesta**: Latencia de las operaciones de API
5. **Satisfacción del Usuario**: Reducción de llamadas al call center

### Métricas Técnicas
1. **Uptime**: Disponibilidad del sistema
2. **Precisión de NLU**: Tasa de reconocimiento correcto de intents
3. **Uso de Fallback**: Frecuencia de mensajes no entendidos
4. **Errores de API**: Tasa de fallos en integraciones
5. **Performance**: Tiempo de respuesta del bot

## Beneficios del Negocio

### Eficiencia Operacional
- **Reducción de Carga Manual**: Automatización de confirmaciones
- **Mejor Planificación**: Información en tiempo real sobre citas
- **Optimización de Recursos**: Reducción de no-shows

### Experiencia del Paciente
- **Comunicación 24/7**: Disponibilidad continua
- **Respuestas Inmediatas**: Sin esperas en call center
- **Facilidad de Uso**: Interfaz conversacional natural
- **Flexibilidad**: Opciones de confirmación, cancelación y reagendamiento

### Escalabilidad
- **Manejo de Volumen**: Procesamiento automático de múltiples conversaciones
- **Integración Robusta**: Conexión confiable con sistemas existentes
- **Mantenimiento Bajo**: Sistema autónomo con monitoreo

## Roadmap del Producto

### Fase Actual (Completada)
- ✅ Confirmación y cancelación de citas
- ✅ Reagendamiento de citas
- ✅ Sistema de fallback inteligente
- ✅ Integración completa con WhatsApp y RedSalud

### Fase 2 (Próximas 4-6 semanas)
- 🔄 Notificaciones push avanzadas
- 🔄 Integración con calendario del paciente
- 🔄 Reportes de uso y analytics
- 🔄 Dashboard de administración

### Fase 3 (Próximas 8-12 semanas)
- 📋 Integración con múltiples canales (SMS, email)
- 📋 IA avanzada para predicción de cancelaciones
- 📋 Sistema de recordatorios personalizados
- 📋 Integración con sistemas de pago

### Fase 4 (Largo plazo)
- 📋 Chatbot multilingüe
- 📋 Integración con wearables y IoT
- 📋 Predicción de salud preventiva
- 📋 Integración con telemedicina

## Casos de Uso Principales

### Caso 1: Confirmación de Cita
**Usuario**: Paciente con cita programada
**Necesidad**: Confirmar asistencia a cita médica
**Solución**: Bot envía mensaje con detalles y opciones de confirmación/cancelación
**Resultado**: Cita confirmada y sistema actualizado automáticamente

### Caso 2: Reagendamiento de Cita
**Usuario**: Paciente que necesita cambiar fecha/hora
**Necesidad**: Reagendar cita médica
**Solución**: Bot ofrece opciones de reagendamiento con botones interactivos
**Resultado**: Proceso de reagendamiento iniciado y confirmado

### Caso 3: Cancelación de Cita
**Usuario**: Paciente que no puede asistir
**Necesidad**: Cancelar cita médica
**Solución**: Bot facilita cancelación con razón específica
**Resultado**: Cita cancelada y slot liberado para otros pacientes

### Caso 4: Mensaje No Entendido
**Usuario**: Paciente envía mensaje confuso
**Necesidad**: Entender qué opciones están disponibles
**Solución**: Bot proporciona ayuda contextual y opciones disponibles
**Resultado**: Usuario recibe orientación útil y puede continuar

## Valor Proporcionado

### Para Pacientes
- **Conveniencia**: Confirmación rápida desde WhatsApp
- **Claridad**: Información clara sobre citas
- **Flexibilidad**: Opciones de confirmación, cancelación y reagendamiento
- **Accesibilidad**: Interfaz familiar y fácil de usar

### Para Personal Médico
- **Eficiencia**: Reducción de trabajo administrativo
- **Planificación**: Mejor visibilidad de confirmaciones
- **Optimización**: Reducción de no-shows
- **Enfoque**: Más tiempo para atención médica

### Para RedSalud
- **Automatización**: Procesos manuales automatizados
- **Escalabilidad**: Manejo de mayor volumen de pacientes
- **Calidad**: Mejor experiencia del paciente
- **ROI**: Reducción de costos operacionales 