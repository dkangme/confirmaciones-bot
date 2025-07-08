"""
Módulo de acciones personalizadas para el bot de confirmaciones.
Implementa la lógica de negocio para manejo de citas y confirmaciones.
"""

import logging
import os
import re
from typing import Any, Text, Dict, List
from datetime import datetime, timedelta
import base64
import requests
from dotenv import load_dotenv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

# Importar módulos locales
from .database import db_connection
from .utils import (
    log_request_info, get_slot_value, extract_entity_value,
    create_json_response, ValidationError, validate_required_fields,
    sanitize_string, format_date_for_display, format_time_for_display
)

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar logger
logger = logging.getLogger(__name__)

# Configuración global para APIGEE
REDSALUD_CONFIG = {
    "auth_url": os.getenv("APIGEE_API_URL") + "/oauth/token" if os.getenv("APIGEE_API_URL") else None,
    "base_url": os.getenv("APIGEE_API_URL"),
    "client_id": os.getenv("APIGEE_USERNAME"),
    "client_secret": os.getenv("APIGEE_PASSWORD")
}

# Log de configuración (sin mostrar credenciales completas)
logger.info(f"APIGEE_API_URL: {os.getenv('APIGEE_API_URL', 'No configurado')}")
logger.info(f"APIGEE_USERNAME: {os.getenv('APIGEE_USERNAME', 'No configurado')[:4]}..." if os.getenv('APIGEE_USERNAME') else "APIGEE_USERNAME: No configurado")
logger.info(f"APIGEE_PASSWORD: {'Configurado' if os.getenv('APIGEE_PASSWORD') else 'No configurado'}")

# Caché para el token de acceso
TOKEN_CACHE = {
    "access_token": None,
    "expires_at": None
}


def obtener_access_token():
    """
    Obtiene un token de acceso para la API de RedSalud.
    Utiliza las credenciales almacenadas en variables de entorno.
    Implementa un mecanismo de caché para evitar solicitudes innecesarias.
    """
    global TOKEN_CACHE

    try:
        # Verificar si hay un token en caché y si aún es válido
        current_time = datetime.now()
        if (TOKEN_CACHE["access_token"] is not None and
            TOKEN_CACHE["expires_at"] is not None and
            current_time < TOKEN_CACHE["expires_at"]):
            logger.info("Usando token de acceso en caché")
            return TOKEN_CACHE["access_token"]

        # Si no hay token o está expirado, solicitar uno nuevo
        if not REDSALUD_CONFIG:
            logger.error("Configuración de RedSalud no disponible")
            return None

        auth_url = REDSALUD_CONFIG.get("auth_url")
        client_id = REDSALUD_CONFIG.get("client_id")
        client_secret = REDSALUD_CONFIG.get("client_secret")

        # Verificar que todas las credenciales estén presentes
        if not all([auth_url, client_id, client_secret]):
            missing = []
            if not auth_url: missing.append("auth_url")
            if not client_id: missing.append("client_id")
            if not client_secret: missing.append("client_secret")
            logger.error(f"Faltan credenciales: {', '.join(missing)}")
            return None

        # Crear el token de autorización Basic usando UTF-8
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        base64_auth = base64.b64encode(auth_bytes).decode('utf-8')

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64_auth}"
        }
        data = {
            "grant_type": "client_credentials"
        }

        logger.info(f"Solicitando token de acceso a {auth_url}")
        logger.info(f"Client ID: {client_id[:4]}...")  # Solo mostrar primeros 4 caracteres por seguridad

        response = requests.post(auth_url, headers=headers, data=data, timeout=120)

        if response.status_code == 200:
            try:
                response_json = response.json()
                access_token = response_json.get("access_token")
                # Asegurarse de que expires_in sea un entero
                expires_in = int(response_json.get("expires_in", 21600))  # 6 horas por defecto (21600 segundos)

                # Calcular tiempo de expiración (5 horas y 45 minutos para tener margen)
                expires_at = current_time + timedelta(seconds=expires_in - 900)

                # Actualizar caché
                TOKEN_CACHE["access_token"] = access_token
                TOKEN_CACHE["expires_at"] = expires_at

                logger.info(f"Token de acceso obtenido exitosamente, expira en {expires_at}")
                return access_token
            except (ValueError, TypeError) as e:
                logger.error(f"Error al procesar la respuesta del token: {e}")
                return None
        else:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = str(error_json)
            except:
                pass
            logger.error(f"Error en la autenticación: {response.status_code} - {error_detail}")
            return None
    except Exception as e:
        logger.error(f"Error al obtener token de acceso: {e}")
        return None


def confirm_appointment(access_token, appointment_id):
    """
    Confirma una cita médica en la API de RedSalud.

    :param access_token: Token de acceso a la API
    :param appointment_id: ID de la cita a confirmar
    :return: Respuesta de la API o diccionario con error
    """
    try:
        if not REDSALUD_CONFIG or not REDSALUD_CONFIG.get("base_url"):
            logger.error("Configuración de RedSalud incompleta o no disponible")
            return {"error": "Configuración de RedSalud incompleta"}

        url = f"{REDSALUD_CONFIG['base_url']}/agendarsv2/cita/confirmar/"

        if not access_token:
            raise ValueError("Token de acceso no válido")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        data = {
            "AppointmentId": appointment_id
        }

        logger.info(f"Solicitando confirmación de cita {appointment_id}")
        response = requests.post(url, headers=headers, json=data, timeout=120)

        if response.status_code == 200:
            try:
                logger.info("Confirmación de cita exitosa")
                return response.json()
            except ValueError:
                logger.error("Respuesta no es un JSON válido")
                return {"error": "Respuesta no es un JSON válido"}
        else:
            logger.error(f"Error al confirmar cita: {response.status_code} - {response.text}")
            return {"error": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        logger.error(f"Excepción al confirmar cita: {e}")
        return {"error": str(e)}


def cancel_appointment(access_token, appointment_id, transition_reason_id, transition_reason_others=""):
    """
    Cancela una cita médica en la API de RedSalud.

    :param access_token: Token de acceso a la API
    :param appointment_id: ID de la cita a cancelar
    :param transition_reason_id: ID del motivo de cancelación
    :param transition_reason_others: Motivo adicional (opcional)
    :return: Respuesta de la API o diccionario con error
    """
    try:
        if not REDSALUD_CONFIG or not REDSALUD_CONFIG.get("base_url"):
            logger.error("Configuración de RedSalud incompleta o no disponible")
            return {"error": "Configuración de RedSalud incompleta"}

        url = f"{REDSALUD_CONFIG['base_url']}/agendarsv2/cita/anular/"

        if not access_token:
            raise ValueError("Token de acceso no válido")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        data = {
            "AppointmentId": appointment_id,
            "AppointmentTransitionReasonId": transition_reason_id,
            "TransitionReasonOthers": transition_reason_others
        }

        logger.info(f"Solicitando cancelación de cita {appointment_id}")
        response = requests.post(url, headers=headers, json=data, timeout=90)

        if response.status_code == 200:
            try:
                logger.info("Cancelación de cita exitosa")
                return response.json()
            except ValueError:
                logger.error("Respuesta no es un JSON válido")
                # A pesar del error de formato, la operación fue exitosa (status 200)
                # Retornamos un objeto que indica éxito pero con un aviso sobre el formato
                return {"success": True, "warning": "Respuesta no es un JSON válido pero la operación fue exitosa"}
        else:
            logger.error(f"Error al cancelar cita: {response.status_code} - {response.text}")
            return {"error": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        logger.error(f"Excepción al cancelar cita: {e}")
        return {"error": str(e)}


class ActionTestConnection(Action):
    """
    Acción para probar la conexión a la base de datos.
    Útil para debugging y verificación del sistema.
    """
    
    def name(self) -> Text:
        return "action_test_connection"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Probar conexión a la base de datos
            connection_success = db_connection.test_connection()
            
            if connection_success:
                message = "✅ Conexión a la base de datos exitosa"
                logger.info("Conexión a BD probada exitosamente")
            else:
                message = "❌ Error en la conexión a la base de datos"
                logger.error("Error en conexión a BD")
            
            dispatcher.utter_message(text=message)
            
            return []
            
        except Exception as e:
            error_message = f"Error probando conexión: {str(e)}"
            logger.error(error_message, exc_info=True)
            dispatcher.utter_message(text="❌ Error interno del sistema")
            return []


class ActionGetSystemStatus(Action):
    """
    Acción para obtener el estado general del sistema.
    Proporciona información sobre la salud del bot y sus componentes.
    """
    
    def name(self) -> Text:
        return "action_get_system_status"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Verificar conexión a BD
            db_status = db_connection.test_connection()
            
            # Crear respuesta de estado
            status_data = {
                "database": "✅ Conectado" if db_status else "❌ Desconectado",
                "bot_version": "3.6.21",
                "user_id": tracker.sender_id,
                "session_active": True
            }
            
            # Crear mensaje de estado
            status_message = f"""
🤖 **Estado del Sistema**

📊 Base de Datos: {status_data['database']}
🔧 Versión del Bot: {status_data['bot_version']}
👤 Usuario: {status_data['user_id']}
🟢 Sesión: Activa
            """.strip()
            
            dispatcher.utter_message(text=status_message)
            
            return []
            
        except Exception as e:
            error_message = f"Error obteniendo estado del sistema: {str(e)}"
            logger.error(error_message, exc_info=True)
            dispatcher.utter_message(text="❌ Error obteniendo estado del sistema")
            return []


class ActionValidateInput(Action):
    """
    Acción para validar entradas del usuario.
    Valida que los datos proporcionados sean correctos antes de procesarlos.
    """
    
    def name(self) -> Text:
        return "action_validate_input"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener datos del último mensaje
            latest_message = tracker.latest_message
            
            # Extraer entidades
            entities = latest_message.get('entities', [])
            
            # Validar que haya entidades para procesar
            if not entities:
                dispatcher.utter_message(text="Por favor proporciona la información requerida")
                return []
            
            # Procesar cada entidad
            validation_results = []
            for entity in entities:
                entity_name = entity.get('entity')
                entity_value = entity.get('value')
                
                if entity_name and entity_value:
                    # Sanitizar valor
                    sanitized_value = sanitize_string(str(entity_value))
                    
                    # Guardar en slot correspondiente
                    validation_results.append(SlotSet(entity_name, sanitized_value))
                    
                    logger.info(f"Entidad validada: {entity_name} = {sanitized_value}")
            
            # Confirmar validación exitosa
            dispatcher.utter_message(text="✅ Información validada correctamente")
            
            return validation_results
            
        except Exception as e:
            error_message = f"Error validando entrada: {str(e)}"
            logger.error(error_message, exc_info=True)
            dispatcher.utter_message(text="❌ Error validando la información proporcionada")
            return []


class ActionHandleError(Action):
    """
    Acción para manejar errores de forma consistente.
    Proporciona respuestas amigables cuando ocurren errores.
    """
    
    def name(self) -> Text:
        return "action_handle_error"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener información del error si está disponible
            error_info = get_slot_value(tracker, "error_info", "Error desconocido")
            
            # Crear mensaje de error amigable
            error_message = f"""
❌ **Error del Sistema**

Lo sentimos, ha ocurrido un error procesando tu solicitud.

🔧 **Detalles técnicos:**
{error_info}

🔄 **Sugerencias:**
• Intenta nuevamente en unos momentos
• Verifica que la información proporcionada sea correcta
• Si el problema persiste, contacta al soporte técnico
            """.strip()
            
            dispatcher.utter_message(text=error_message)
            
            # Limpiar información de error
            return [SlotSet("error_info", None)]
            
        except Exception as e:
            logger.error(f"Error en action_handle_error: {str(e)}", exc_info=True)
            dispatcher.utter_message(text="❌ Error interno del sistema")
            return []


class ActionFallback(Action):
    """
    Acción de fallback cuando el bot no entiende la intención del usuario.
    Proporciona ayuda y opciones al usuario.
    """
    
    def name(self) -> Text:
        return "action_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener el mensaje del usuario
            user_message = tracker.latest_message.get('text', '')
            
            fallback_message = f"""
🤖 **No entiendo tu solicitud**

Tu mensaje: "{user_message}"

💡 **Puedo ayudarte con:**
• Confirmar citas médicas
• Cancelar citas
• Reprogramar citas
• Proporcionar información de citas

📝 **Ejemplos de comandos:**
• "Quiero confirmar mi cita"
• "Necesito cancelar mi cita"
• "Quiero reprogramar mi cita para mañana"

¿En qué puedo ayudarte?
            """.strip()
            
            dispatcher.utter_message(text=fallback_message)
            
            return []
            
        except Exception as e:
            logger.error(f"Error en action_fallback: {str(e)}", exc_info=True)
            dispatcher.utter_message(text="❌ Error interno del sistema")
            return []


class ActionInitContext(Action):
    """
    Acción para inicializar el contexto de confirmación.
    Actualiza todos los slots con la información de la cita y configura el contexto.
    """
    
    def name(self) -> Text:
        return "action_init_context"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener entidades del último mensaje
            entities = tracker.latest_message.get('entities', [])
            
            # Lista para almacenar todos los eventos de slots
            slot_events = []
            
            # Procesar cada entidad y actualizar el slot correspondiente
            for entity in entities:
                entity_name = entity.get('entity')
                entity_value = entity.get('value')
                
                if entity_name and entity_value is not None:
                    # Sanitizar el valor si es string
                    if isinstance(entity_value, str):
                        sanitized_value = sanitize_string(entity_value)
                    else:
                        sanitized_value = entity_value
                    
                    # Crear evento para actualizar el slot
                    slot_events.append(SlotSet(entity_name, sanitized_value))
                    
                    logger.info(f"Slot actualizado: {entity_name} = {sanitized_value}")
            
            # Configurar el contexto como "confirmación"
            slot_events.append(SlotSet("contexto", "confirmación"))
            logger.info("Contexto configurado como: confirmación")
            
            # Limpiar el contexto de rebooking para evitar conflictos
            slot_events.append(SlotSet("contexto_rebooking", None))
            logger.info("Contexto de rebooking limpiado")
            
            # Formatear fecha_hora si está disponible
            fecha_hora = get_slot_value(tracker, "fecha_hora")
            if fecha_hora:
                try:
                    # Parsear la fecha ISO y formatearla
                    from datetime import datetime
                    fecha_obj = datetime.fromisoformat(fecha_hora.replace('Z', '+00:00'))
                    fecha_formateada = fecha_obj.strftime("%d/%m/%Y a las %H:%M")
                    slot_events.append(SlotSet("fecha_hora_formato", fecha_formateada))
                    logger.info(f"Fecha formateada: {fecha_formateada}")
                except Exception as e:
                    logger.warning(f"Error formateando fecha: {str(e)}")
                    slot_events.append(SlotSet("fecha_hora_formato", fecha_hora))
            
            # Crear mensaje de confirmación
            confirmation_message = f"""
✅ **Contexto Inicializado Correctamente**

🔄 **Información Procesada:**
• Entidades recibidas: {len(entities)}
• Slots actualizados: {len(slot_events)}
• Contexto: confirmación

📋 **Detalles de la Cita:**
"""
            
            # Agregar información específica si está disponible
            nombre_paciente = get_slot_value(tracker, "nombre_paciente")
            especialidad = get_slot_value(tracker, "especialidad")
            centro_medico = get_slot_value(tracker, "centro_medico")
            
            if nombre_paciente:
                confirmation_message += f"• Paciente: {nombre_paciente}\n"
            if especialidad:
                confirmation_message += f"• Especialidad: {especialidad}\n"
            if fecha_hora:
                confirmation_message += f"• Fecha/Hora: {fecha_hora}\n"
            if centro_medico:
                confirmation_message += f"• Centro Médico: {centro_medico}\n"
            
            confirmation_message += "\n🎯 **Sistema listo para confirmaciones**"
            
            dispatcher.utter_message(text=confirmation_message)
            
            logger.info(f"Contexto inicializado exitosamente para usuario: {tracker.sender_id}")
            
            return slot_events
            
        except Exception as e:
            error_message = f"Error inicializando contexto: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            # Guardar información del error en un slot
            error_events = [SlotSet("error_info", error_message)]
            
            dispatcher.utter_message(text="❌ Error inicializando el contexto del sistema")
            
            return error_events


class ActionFormatDate(Action):
    """
    Acción para formatear la fecha y hora para mostrar al usuario en español, por ejemplo:
    'miércoles 2 de julio de 2025 a las 13:30'
    """
    
    def name(self) -> Text:
        return "action_format_date"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener fecha_hora del slot
            fecha_hora = get_slot_value(tracker, "fecha_hora")
            
            if not fecha_hora:
                logger.warning("No se encontró fecha_hora para formatear")
                return []
            
            from datetime import datetime
            dias_semana = [
                "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
            ]
            meses = [
                "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
            ]
            # Parsear la fecha ISO
            fecha_obj = datetime.fromisoformat(fecha_hora.replace('Z', '+00:00'))
            dia_semana = dias_semana[fecha_obj.weekday()]
            dia = fecha_obj.day
            mes = meses[fecha_obj.month - 1]
            anio = fecha_obj.year
            hora = fecha_obj.strftime("%H:%M")
            fecha_formateada = f"{dia_semana} {dia} de {mes} de {anio} a las {hora}"
            
            # Actualizar el slot
            slot_event = SlotSet("fecha_hora_formato", fecha_formateada)
            
            logger.info(f"Fecha formateada: {fecha_formateada}")
            
            return [slot_event]
            
        except Exception as e:
            error_message = f"Error formateando fecha: {str(e)}"
            logger.error(error_message, exc_info=True)
            return []


class ActionCancelAppointment(Action):
    """
    Acción para cancelar una cita usando la API de Apigee.
    Obtiene el token de Apigee y llama a cancel_appointment con ese token.
    """
    
    def name(self) -> Text:
        return "action_cancel_appointment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener información de la cita desde los slots
            nombre_paciente = get_slot_value(tracker, "nombre_paciente")
            fecha_hora = get_slot_value(tracker, "fecha_hora")
            resource_name = get_slot_value(tracker, "resource_name")
            centro_medico = get_slot_value(tracker, "centro_medico")
            appointment_id = get_slot_value(tracker, "conversation_id")  # appointment_id se obtiene del slot conversation_id
            
            # Verificar que tenemos la información necesaria
            if not all([nombre_paciente, fecha_hora, resource_name, centro_medico]):
                logger.warning("Información incompleta para cancelar cita")
                dispatcher.utter_message(text="❌ No se pudo procesar la cancelación. Información incompleta.")
                return []
            
            if not appointment_id:
                logger.warning("No se encontró appointment_id para cancelar en Apigee")
                # Continuar con la cancelación local aunque no se pueda cancelar en Apigee
            else:
                # Obtener token de acceso de Apigee
                access_token = obtener_access_token()
                
                if access_token:
                    # Cancelar cita usando la API de Apigee
                    # Usar un motivo de cancelación por defecto (ajustar según necesidades)
                    transition_reason_id = 1  # Motivo por defecto - ajustar según la configuración de Apigee
                    transition_reason_others = "Cancelación solicitada por paciente"
                    
                    result = cancel_appointment(access_token, appointment_id, transition_reason_id, transition_reason_others)
                    
                    if "error" in result:
                        logger.error(f"Error cancelando cita en Apigee: {result['error']}")
                        
                        # Actualizar estado en base de datos como error
                        if appointment_id:
                            db_connection.update_appointment_status(appointment_id, "canceled error")
                        
                        # Enviar mensaje de error directamente
                        dispatcher.utter_message(response="utter_cancel_appointment_failed")
                        logger.info(f"Cancelación fallida para usuario: {tracker.sender_id}")
                        return []
                    else:
                        logger.info(f"Cita cancelada exitosamente en Apigee: {result}")
                        
                        # Actualizar estado en base de datos como cancelado
                        if appointment_id:
                            db_connection.update_appointment_status(appointment_id, "canceled")
                        
                        # Obtener área médica para determinar qué mensaje enviar
                        area_medica = get_slot_value(tracker, "area_medica")
                        
                        # Enviar mensaje según el área médica
                        if area_medica and area_medica.lower() == "dental":
                            dispatcher.utter_message(response="utter_confirm_dental_rejection")
                        else:
                            dispatcher.utter_message(response="utter_confirm_rejection")
                        
                        logger.info(f"Cancelación exitosa para usuario: {tracker.sender_id}")
                        return []
                else:
                    logger.warning("No se pudo obtener token de acceso para Apigee")
                    # Enviar mensaje de error directamente
                    dispatcher.utter_message(response="utter_cancel_appointment_failed")
                    logger.info(f"Cancelación fallida (sin token) para usuario: {tracker.sender_id}")
                    return []
            
            # Si no hay appointment_id, enviar mensaje de error
            dispatcher.utter_message(response="utter_cancel_appointment_failed")
            logger.info(f"Cancelación fallida (sin appointment_id) para usuario: {tracker.sender_id}")
            return []
            
        except Exception as e:
            error_message = f"Error cancelando cita: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            # Guardar información del error en un slot
            error_events = [SlotSet("error_info", error_message)]
            
            dispatcher.utter_message(text="❌ Error procesando la cancelación de la cita")
            
            return error_events


class ActionConfirmAppointment(Action):
    """
    Acción para confirmar una cita médica en RedSalud.
    """
    
    def name(self) -> Text:
        return "action_confirm_appointment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener información de la cita
            nombre_paciente = get_slot_value(tracker, "nombre_paciente")
            fecha_hora = get_slot_value(tracker, "fecha_hora")
            resource_name = get_slot_value(tracker, "resource_name")
            centro_medico = get_slot_value(tracker, "centro_medico")
            appointment_id = get_slot_value(tracker, "conversation_id")  # appointment_id se obtiene del slot conversation_id
            
            # Verificar que tenemos la información necesaria
            if not all([nombre_paciente, fecha_hora, resource_name, centro_medico]):
                logger.warning("Información incompleta para confirmar cita")
                dispatcher.utter_message(text="❌ No se pudo procesar la confirmación. Información incompleta.")
                return []
            
            # Obtener el ID de la cita desde los slots
            if not appointment_id:
                logger.warning("No se encontró appointment_id para confirmar en RedSalud")
                # Continuar con la confirmación local aunque no se pueda confirmar en RedSalud
            else:
                # Obtener token de acceso para RedSalud
                access_token = obtener_access_token()
                
                if access_token:
                    # Confirmar cita en RedSalud
                    result = confirm_appointment(access_token, appointment_id)
                    
                    if "error" in result:
                        logger.error(f"Error confirmando cita en Apigee: {result['error']}")
                        
                        # Actualizar estado en base de datos como error
                        if appointment_id:
                            db_connection.update_appointment_status(appointment_id, "confirmed error")
                        
                        # Enviar mensaje de error directamente
                        dispatcher.utter_message(response="utter_confirmation_appointment_failed")
                        logger.info(f"Confirmación fallida para usuario: {tracker.sender_id}")
                        return []
                    else:
                        logger.info(f"Cita confirmada exitosamente en Apigee: {result}")
                        
                        # Actualizar estado en base de datos como confirmado
                        if appointment_id:
                            db_connection.update_appointment_status(appointment_id, "confirmed")
                        
                        # Obtener slots para determinar qué mensajes enviar
                        especialidad = get_slot_value(tracker, "especialidad")
                        area_medica = get_slot_value(tracker, "area_medica")
                        centro_medico_tipo = get_slot_value(tracker, "centro_medico_tipo")
                        
                        # Verificar si es área dental
                        is_dental = (area_medica and area_medica.lower() == "dental")
                        
                        if is_dental:
                            # Enviar mensajes específicos para dental
                            dispatcher.utter_message(response="utter_confirm_dental_header")
                            dispatcher.utter_message(response="utter_confirm_dental_footer")
                        else:
                            # Lógica existente para áreas no-dental
                            # Siempre enviar header y footer
                            dispatcher.utter_message(response="utter_confirm_header")
                            
                            # Verificar condiciones para mensajes adicionales
                            # Evaluar especialidad
                            is_medicina_general = (especialidad and 
                                                 ("general" in especialidad.lower() or 
                                                  "medicina general" in especialidad.lower()))
                            
                            # Evaluar área médica
                            is_area_medica = (area_medica and area_medica.lower() == "medica")
                            
                            # Evaluar tipo de centro médico
                            is_centro_medico = (centro_medico_tipo and centro_medico_tipo.lower() == "centro")
                            
                            # Enviar mensaje de centro médico si es área médica y centro médico
                            if is_area_medica and is_centro_medico:
                                dispatcher.utter_message(response="utter_confirm_centro_medico")
                            
                            # Enviar mensaje de medicina general si es medicina general y área médica
                            if is_medicina_general and is_area_medica:
                                dispatcher.utter_message(response="utter_confirm_medicina_general")
                            
                            # Siempre enviar footer
                            dispatcher.utter_message(response="utter_confirm_footer")
                        
                        logger.info(f"Confirmación exitosa para usuario: {tracker.sender_id}")
                        return []
                else:
                    logger.warning("No se pudo obtener token de acceso para Apigee")
                    # Enviar mensaje de error directamente
                    dispatcher.utter_message(response="utter_confirmation_appointment_failed")
                    logger.info(f"Confirmación fallida (sin token) para usuario: {tracker.sender_id}")
                    return []
            
            # Si no hay appointment_id, enviar mensaje de error
            dispatcher.utter_message(response="utter_confirmation_appointment_failed")
            logger.info(f"Confirmación fallida (sin appointment_id) para usuario: {tracker.sender_id}")
            return []
            
        except Exception as e:
            error_message = f"Error confirmando cita: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            # Guardar información del error en un slot
            error_events = [SlotSet("error_info", error_message)]
            
            dispatcher.utter_message(text="❌ Error procesando la confirmación de la cita")
            
            return error_events


