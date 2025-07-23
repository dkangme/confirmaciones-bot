"""
Módulo de acciones personalizadas para rebooking de citas.
Implementa la lógica de negocio para el reagendamiento de citas médicas.
"""

import logging
import urllib.parse
import requests
import json
from typing import Any, Text, Dict, List, Optional
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

# Importar módulos locales
from .utils import log_request_info, get_slot_value, sanitize_string

# Configurar logger
logger = logging.getLogger(__name__)


# ===== FUNCIONES DE REBOOKING =====

def get_slots_optimized(
    resource_id: str,
    service_id: str,
    coverage_plan_id: str,
    start_time: str,
    finish_time: str,
    adjacent_slots: int,
    patient_id: str,
    include_self_payer: bool = False,
    expert_booking_mode: bool = False,
    include_not_bookable: bool = False,
    reschedule_appointment_id: str = None,
    app_timezone: int = -240,
    auth_token: str = "pkiALQixUCgj1LrLz0fpC7NiMUoJ"
) -> Dict:
    """
    Obtiene slots optimizados de la API de RedSalud.
    
    Args:
        resource_id (str): ID del recurso
        service_id (str): ID del servicio
        coverage_plan_id (str): ID del plan de cobertura
        start_time (str): Tiempo de inicio en formato ISO
        finish_time (str): Tiempo de fin en formato ISO
        adjacent_slots (int): Número de slots adyacentes
        patient_id (str): ID del paciente
        include_self_payer (bool): Incluir pagos propios
        expert_booking_mode (bool): Modo de reserva experto
        include_not_bookable (bool): Incluir no reservables
        reschedule_appointment_id (str): ID de la cita a reagendar
        app_timezone (int): Zona horaria de la aplicación
        auth_token (str): Token de autorización
        
    Returns:
        Dict: Respuesta de la API
    """
    base_url = "https://proxy-qa.redsalud.cl/AWAUsers/Slots/GetSlotsOptimized"
    
    # Construir parámetros de la URL (corresponden a los parámetros de función en el curl)
    # Orden correcto según el curl: includeSelfPayer, expertBookingMode, includeNotBookable, rescheduleAppointmentId
    params = {
        "includeSelfPayer": str(include_self_payer).lower(),
        "expertBookingMode": str(expert_booking_mode).lower(),
        "includeNotBookable": str(include_not_bookable).lower(),
        "rescheduleAppointmentId": reschedule_appointment_id
    }
    
    if reschedule_appointment_id:
        params["rescheduleAppointmentId"] = reschedule_appointment_id
    
    # Construir filtro (corresponde al $filter en el curl)
    filter_parts = [
        f"ResourceId eq {resource_id}",
        f"ServiceId eq {service_id}",
        f"CoveragePlanId eq {coverage_plan_id}",
        f"(StartTime ge {start_time})",
        f"(FinishTime le {finish_time})",
        f"AdjacentSlots eq {adjacent_slots}",
        f"PatientId eq {patient_id}"
    ]
    
    filter_str = " and ".join(filter_parts)
    
    # Construir URL completa (corresponde exactamente al formato del curl)
    # Formato: base_url(param1=value1,param2=value2)?$filter=...&$orderby=...&$count=true
    url = f"{base_url}({','.join(f'{k}={v}' for k, v in params.items())})"
    url += f"?$filter={urllib.parse.quote(filter_str)}"
    url += "&$orderby=StartTime asc&$count=true"
    
    # Log de la URL generada
    logger.info(f"🌐 URL generada para get_slots_optimized:")
    logger.info(f"   Base URL: {base_url}")
    logger.info(f"   Parámetros: {params}")
    logger.info(f"   Filtro: {filter_str}")
    logger.info(f"   URL completa: {url}")
    
    # Headers
    headers = {
        "X-AppTimezone": str(app_timezone),
        "Authorization": f"Bearer {auth_token}"
    }
    
    # Log de headers (sin el token por seguridad)
    logger.info(f"📋 Headers de la petición:")
    logger.info(f"   X-AppTimezone: {app_timezone}")
    logger.info(f"   Authorization: Bearer [TOKEN_OCULTO]")
    
    try:
        logger.info(f"🚀 Enviando petición GET a la API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Log de la respuesta
        logger.info(f"✅ Respuesta exitosa de la API:")
        logger.info(f"   Status Code: {response.status_code}")
        logger.info(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        response_data = response.json()
        
        # Log detallado de la respuesta exitosa
        logger.info(f"✅ RESPUESTA EXITOSA DE get_slots_optimized:")
        logger.info(f"   Status Code: {response.status_code}")
        logger.info(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        logger.info(f"   Content-Length: {response.headers.get('content-length', 'N/A')}")
        
        if response_data:
            logger.info(f"📊 ESTRUCTURA DE LA RESPUESTA:")
            logger.info(f"   Claves principales: {list(response_data.keys())}")
            
            if "slots" in response_data:
                slots_count = len(response_data["slots"])
                logger.info(f"   Número total de slots: {slots_count}")
                
                # Contar slots disponibles
                available_slots = [slot for slot in response_data["slots"] if slot.get("Bookable", {}).get("Bookable", False)]
                logger.info(f"   Slots disponibles: {len(available_slots)}")
                logger.info(f"   Slots no disponibles: {slots_count - len(available_slots)}")
                
                # Mostrar detalles de los primeros 5 slots
                logger.info(f"📅 DETALLES DE SLOTS (primeros 5):")
                for i, slot in enumerate(response_data["slots"][:5]):
                    timestamp = slot.get("Timestamp")
                    bookable = slot.get("Bookable", {}).get("Bookable", False)
                    start_time = slot.get("StartTime")
                    end_time = slot.get("EndTime")
                    resource_id = slot.get("ResourceId")
                    
                    # Convertir timestamp a fecha legible si existe
                    fecha_legible = ""
                    if timestamp:
                        try:
                            from datetime import datetime
                            dt = datetime.fromtimestamp(timestamp)
                            fecha_legible = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            fecha_legible = "Error parsing timestamp"
                    
                    logger.info(f"   Slot {i+1}:")
                    logger.info(f"     - Timestamp: {timestamp} ({fecha_legible})")
                    logger.info(f"     - Bookable: {bookable}")
                    logger.info(f"     - StartTime: {start_time}")
                    logger.info(f"     - EndTime: {end_time}")
                    logger.info(f"     - ResourceId: {resource_id}")
                
                if slots_count > 5:
                    logger.info(f"   ... y {slots_count - 5} slots más")
                
                # Mostrar estadísticas adicionales
                if available_slots:
                    logger.info(f"📈 ESTADÍSTICAS DE SLOTS DISPONIBLES:")
                    timestamps_disponibles = [slot.get("Timestamp") for slot in available_slots if slot.get("Timestamp")]
                    if timestamps_disponibles:
                        from datetime import datetime
                        fechas_disponibles = [datetime.fromtimestamp(ts) for ts in timestamps_disponibles]
                        fechas_unicas = list(set([fecha.strftime("%Y-%m-%d") for fecha in fechas_disponibles]))
                        logger.info(f"     - Fechas únicas disponibles: {len(fechas_unicas)}")
                        logger.info(f"     - Fechas: {fechas_unicas[:3]}{'...' if len(fechas_unicas) > 3 else ''}")
            else:
                logger.info(f"   Respuesta sin slots: {list(response_data.keys())}")
                logger.info(f"   Contenido completo: {response_data}")
        else:
            logger.warning("⚠️ Respuesta vacía de la API")
        
        # Log final de éxito
        logger.info(f"🎉 get_slots_optimized completado exitosamente")
        logger.info(f"   URL llamada: {url}")
        logger.info(f"   Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ ERROR en get_slots_optimized:")
        logger.error(f"   Tipo de error: {type(e).__name__}")
        logger.error(f"   Mensaje: {str(e)}")
        logger.error(f"   URL que falló: {url}")
        
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"   Status Code: {e.response.status_code}")
            logger.error(f"   Response Headers: {dict(e.response.headers)}")
            logger.error(f"   Response Text: {e.response.text}")
        else:
            logger.error(f"   Sin respuesta del servidor (error de conexión)")
        
        return None


def process_available_slots(slots_response: Dict) -> Optional[List[str]]:
    """
    Procesa la respuesta de la API de slots y retorna una lista de fechas disponibles.
    
    Args:
        slots_response (Dict): Respuesta de la API con los slots disponibles
        
    Returns:
        Optional[List[str]]: Lista de fechas disponibles formateadas o None si no hay slots
    """
    if not slots_response or "slots" not in slots_response:
        logger.debug("No hay slots en la respuesta")
        return None
        
    available_slots = []
    slots = slots_response["slots"]
    
    # Mapeo de días de la semana
    dias_semana = {
        0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
        4: "viernes", 5: "sábado", 6: "domingo"
    }
    
    # Mapeo de meses
    meses = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    # Procesar los primeros 5 slots disponibles
    for slot in slots[:5]:
        if slot.get("Bookable", {}).get("Bookable", False):
            # Convertir timestamp a datetime
            timestamp = slot.get("Timestamp")
            if timestamp:
                dt = datetime.fromtimestamp(timestamp)
                
                # Formatear la fecha
                dia_semana = dias_semana[dt.weekday()]
                dia = dt.day
                mes = meses[dt.month]
                año = dt.year
                hora = dt.strftime("%H:%M")
                
                fecha_formateada = f"{dia_semana} {dia} de {mes} de {año} a las {hora}"
                available_slots.append(fecha_formateada)
    
    if not available_slots:
        logger.debug("No se encontraron slots disponibles")
        return None
        
    logger.debug(f"Slots disponibles encontrados: {len(available_slots)}")
    for slot in available_slots:
        logger.debug(f"Slot disponible: {slot}")
        
    return available_slots


class ActionInitRebooking(Action):
    """
    Acción para inicializar el contexto de rebooking.
    Actualiza todos los slots con la información de la cita y configura el contexto como "rebooking".
    """
    
    def name(self) -> Text:
        return "action_init_rebooking"
    
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
            
            # Copiar conversation_id a appointment_id si existe
            conversation_id = get_slot_value(tracker, "conversation_id")
            if conversation_id:
                slot_events.append(SlotSet("appointment_id", conversation_id))
                logger.info(f"Conversation ID copiado a appointment_id: {conversation_id}")
            else:
                logger.warning("No se encontró conversation_id para copiar a appointment_id")
            
            # Configurar el contexto de rebooking
            slot_events.append(SlotSet("contexto_rebooking", "rebooking"))
            logger.info("Contexto de rebooking configurado como: rebooking")
            
            # Configurar el contexto general como None para evitar conflictos
            slot_events.append(SlotSet("contexto", None))
            logger.info("Contexto general configurado como: None")
            
            # Configurar el contexto de rebooking menu como None
            slot_events.append(SlotSet("contexto_rebooking_menu", None))
            logger.info("Contexto de rebooking menu configurado como: None")
            
            # Formatear fecha_hora si está disponible
            fecha_hora = get_slot_value(tracker, "fecha_hora")
            if fecha_hora:
                try:
                    # Parsear la fecha ISO y formatearla
                    fecha_obj = datetime.fromisoformat(fecha_hora.replace('Z', '+00:00'))
                    fecha_formateada = fecha_obj.strftime("%d/%m/%Y a las %H:%M")
                    slot_events.append(SlotSet("fecha_hora_formato", fecha_formateada))
                    logger.info(f"Fecha formateada: {fecha_formateada}")
                except Exception as e:
                    logger.warning(f"Error formateando fecha: {str(e)}")
                    slot_events.append(SlotSet("fecha_hora_formato", fecha_hora))
            
            # Crear mensaje de confirmación
            confirmation_message = f"""
✅ **Contexto de Rebooking Inicializado**

🔄 **Información Procesada:**
• Entidades recibidas: {len(entities)}
• Slots actualizados: {len(slot_events)}
• Contexto de rebooking: activo

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
            
            confirmation_message += "\n🎯 **Sistema listo para reagendamiento**"
            
            dispatcher.utter_message(text=confirmation_message)
            
            logger.info(f"Contexto de rebooking inicializado exitosamente para usuario: {tracker.sender_id}")
            
            return slot_events
            
        except Exception as e:
            error_message = f"Error inicializando contexto de rebooking: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            # Guardar información del error en un slot
            error_events = [SlotSet("error_info", error_message)]
            
            dispatcher.utter_message(text="❌ Error inicializando el contexto de rebooking")
            
            return error_events


class ActionProcessDateRequest(Action):
    """
    Acción para procesar las expresiones de fecha y hora del usuario para rebooking.
    Extrae la fecha y hora de expresiones como "mañana a las 10", "el lunes a las 13", etc.
    """
    
    def name(self) -> Text:
        return "action_process_date_request"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener el mensaje del usuario
            user_message = tracker.latest_message.get('text', '').lower()
            logger.info(f"Procesando mensaje: {user_message}")
            
            # Extraer fecha y hora del mensaje
            fecha, hora = self._extract_date_time(user_message)
            
            if fecha and hora:
                # Generar start_time y end_time
                start_time, end_time = self._generate_time_range(fecha, hora)
                
                if start_time and end_time:
                    # Guardar en slots
                    slot_events = [
                        SlotSet("rebooking_fecha", fecha),
                        SlotSet("rebooking_hora", hora),
                        SlotSet("start_time", start_time),
                        SlotSet("end_time", end_time)
                    ]
                    
                    logger.info(f"Fecha y hora extraídas: {fecha} a las {hora}")
                    logger.info(f"Start time: {start_time}")
                    logger.info(f"End time: {end_time}")
                    
                    # Llamar a la función get_slots_optimized con los valores generados
                    slots_response = self._call_get_slots_optimized_with_values(tracker, start_time, end_time)
                    
                    if slots_response:
                        # Guardar la respuesta completa de la API
                        slot_events.append(SlotSet("slots_response", slots_response))
                        
                        # Procesar los slots disponibles
                        available_slots = process_available_slots(slots_response)
                        
                        if available_slots:
                            # Guardar las opciones disponibles en un slot
                            slot_events.append(SlotSet("available_slots", available_slots))
                            
                            # Mostrar confirmación al usuario
                            #confirmation_message = f"Perfecto, entiendo que quieres reagendar para el **{fecha} a las {hora}**. Te mostraré las opciones disponibles."
                            #dispatcher.utter_message(text=confirmation_message)
                            
                            return slot_events
                        else:
                            # No hay slots disponibles
                            error_message = "❌ No hay horarios disponibles para la fecha y hora que solicitas. Por favor, intenta con otra fecha o hora."
                            dispatcher.utter_message(text=error_message)
                            dispatcher.utter_message(response="utter_rebooking_ask_date")
                            return []
                    else:
                        # Error al obtener slots
                        error_message = "❌ Hubo un error al buscar horarios disponibles. Por favor, intenta de nuevo."
                        dispatcher.utter_message(text=error_message)
                        dispatcher.utter_message(response="utter_rebooking_ask_date")
                        return []
                else:
                    # Error al generar fechas
                    error_message = "❌ No se pudo procesar la fecha y hora. Por favor, especifica de forma más clara."
                    dispatcher.utter_message(text=error_message)
                    dispatcher.utter_message(response="utter_rebooking_ask_date")
                    return []
            else:
                # No se pudo entender la fecha/hora
                error_message = "❌ No pude entender el día y la hora que deseas. Por favor, especifica de forma más clara, por ejemplo:\n\n• 'mañana a las 10'\n• 'el lunes a las 13'\n• 'pasado mañana en la tarde'\n• 'el martes 15 a las 11'"
                dispatcher.utter_message(text=error_message)
                
                # Volver a preguntar
                dispatcher.utter_message(response="utter_rebooking_ask_date")
                
                return []
                
        except Exception as e:
            error_message = f"Error procesando fecha y hora: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            dispatcher.utter_message(text="❌ Hubo un error procesando tu solicitud. Por favor, intenta de nuevo.")
            dispatcher.utter_message(response="utter_rebooking_ask_date")
            
            return []
    
    def _extract_date_time(self, message: str) -> tuple:
        """
        Extrae fecha y hora de un mensaje del usuario.
        Retorna (fecha, hora) o (None, None) si no se puede determinar.
        """
        try:
            from datetime import datetime, timedelta
            import re
            
            # Normalizar el mensaje
            message = message.lower().strip()
            
            # Patrones para fechas relativas
            if "mañana" in message:
                fecha_obj = datetime.now() + timedelta(days=1)
                fecha = self._format_date_spanish(fecha_obj)
            elif "pasado mañana" in message:
                fecha_obj = datetime.now() + timedelta(days=2)
                fecha = self._format_date_spanish(fecha_obj)
            else:
                # Buscar días de la semana
                dias_semana = {
                    "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
                    "viernes": 4, "sábado": 5, "domingo": 6
                }
                
                fecha = None
                for dia, numero in dias_semana.items():
                    if dia in message:
                        # Calcular la próxima ocurrencia del día
                        hoy = datetime.now()
                        dias_hasta = (numero - hoy.weekday()) % 7
                        if dias_hasta == 0:  # Si es hoy, tomar la próxima semana
                            dias_hasta = 7
                        fecha_obj = hoy + timedelta(days=dias_hasta)
                        fecha = self._format_date_spanish(fecha_obj)
                        break
                
                if not fecha:
                    return None, None
            
            # Extraer hora
            hora = self._extract_hora(message)
            
            return fecha, hora
            
        except Exception as e:
            logger.error(f"Error extrayendo fecha y hora: {e}")
            return None, None
    
    def _extract_hora(self, message: str) -> str:
        """
        Extrae la hora del mensaje del usuario.
        """
        try:
            import re
            
            # Buscar patrones de hora específica
            hora_patterns = [
                r"a las (\d{1,2}):(\d{2})",  # "a las 10:30"
                r"a las (\d{1,2})",           # "a las 10"
                r"las (\d{1,2}):(\d{2})",    # "las 10:30"
                r"las (\d{1,2})",             # "las 10"
                r"(\d{1,2}):(\d{2})",        # "10:30"
                r"(\d{1,2})",                 # "10"
            ]
            
            for pattern in hora_patterns:
                match = re.search(pattern, message)
                if match:
                    if len(match.groups()) == 2:
                        hora = int(match.group(1))
                        minutos = int(match.group(2))
                    else:
                        hora = int(match.group(1))
                        minutos = 0
                    
                    # Validar hora
                    if 0 <= hora <= 23 and 0 <= minutos <= 59:
                        return f"{hora:02d}:{minutos:02d}"
            
            # Si no hay hora específica, buscar referencias de tiempo
            if "mañana" in message and "tarde" not in message and "noche" not in message:
                return "09:00"
            elif "tarde" in message:
                return "14:00"
            elif "noche" in message:
                return "18:00"
            
            return None
            
        except Exception as e:
            logger.error(f"Error extrayendo hora: {e}")
            return None
    
    def _format_date_spanish(self, fecha_obj: datetime) -> str:
        """
        Formatea una fecha en formato español: "5 de julio"
        """
        try:
            # Nombres de los meses en español
            meses = {
                1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
                5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
                9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
            }
            
            dia = fecha_obj.day
            mes = meses[fecha_obj.month]
            
            return f"{dia} de {mes}"
            
        except Exception as e:
            logger.error(f"Error formateando fecha: {e}")
            return fecha_obj.strftime("%d/%m/%Y")  # Fallback al formato original
    
    def _generate_time_range(self, fecha: str, hora: str) -> tuple:
        """
        Genera start_time y end_time a partir de la fecha y hora extraídas.
        
        Args:
            fecha: Fecha en formato "5 de julio"
            hora: Hora en formato "10:00"
            
        Returns:
            tuple: (start_time, end_time) en formato ISO
        """
        try:
            from datetime import datetime, timedelta
            
            # Convertir fecha y hora a datetime
            fecha_obj = self._parse_spanish_date(fecha)
            if not fecha_obj:
                return None, None
            
            # Parsear hora
            hora_parts = hora.split(':')
            if len(hora_parts) != 2:
                return None, None
            
            hora_int = int(hora_parts[0])
            minutos_int = int(hora_parts[1])
            
            # Crear datetime completo
            fecha_hora_obj = fecha_obj.replace(hour=hora_int, minute=minutos_int, second=0, microsecond=0)
            
            # Generar start_time y end_time
            start_time = fecha_hora_obj.strftime("%Y-%m-%dT%H:%M:%S-04:00")
            end_time = (fecha_hora_obj + timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S-04:00")
            
            return start_time, end_time
            
        except Exception as e:
            logger.error(f"Error generando rango de tiempo: {e}")
            return None, None
    
    def _parse_spanish_date(self, fecha: str) -> datetime:
        """
        Parsea una fecha en formato español a datetime.
        
        Args:
            fecha: Fecha en formato "5 de julio"
            
        Returns:
            datetime: Objeto datetime o None si no se puede parsear
        """
        try:
            # Mapeo de meses
            meses = {
                "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
                "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
                "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
            }
            
            # Parsear "5 de julio"
            parts = fecha.split(" de ")
            if len(parts) != 2:
                return None
            
            dia = int(parts[0])
            mes_nombre = parts[1].lower()
            
            if mes_nombre not in meses:
                return None
            
            mes = meses[mes_nombre]
            año = datetime.now().year
            
            # Si la fecha ya pasó este año, usar el próximo año
            fecha_obj = datetime(año, mes, dia)
            if fecha_obj < datetime.now():
                fecha_obj = datetime(año + 1, mes, dia)
            
            return fecha_obj
            
        except Exception as e:
            logger.error(f"Error parseando fecha española: {e}")
            return None
    
    def _call_get_slots_optimized_with_values(self, tracker: Tracker, start_time: str, end_time: str) -> Dict:
        """
        Llama a la función get_slots_optimized con los parámetros de los slots y valores específicos.
        
        Args:
            tracker: Tracker de RASA
            start_time: Tiempo de inicio en formato ISO
            end_time: Tiempo de fin en formato ISO
            
        Returns:
            Dict: Respuesta de la API o None si hay error
        """
        try:
            # Obtener parámetros de los slots
            resource_id = get_slot_value(tracker, "resource_id") or get_slot_value(tracker, "resource_name")
            service_id = get_slot_value(tracker, "service_id")
            coverage_plan_id = get_slot_value(tracker, "coverage_plan_id", "1")  # Default a 1 si no existe
            adjacent_slots = get_slot_value(tracker, "adjacent_slots", "1")  # Default a 1
            patient_id = get_slot_value(tracker, "patient_id")  # Usar el slot patient_id correcto
            reschedule_appointment_id = get_slot_value(tracker, "reschedule_appointment_id")
            
            # Log de todos los slots para debugging
            logger.info(f"🔍 Debugging slots:")
            logger.info(f"   resource_id: {get_slot_value(tracker, 'resource_id')}")
            logger.info(f"   id_especialidad: {get_slot_value(tracker, 'id_especialidad')}")
            logger.info(f"   autopago: {get_slot_value(tracker, 'autopago')}")
            logger.info(f"   phone_number: {get_slot_value(tracker, 'phone_number')}")
            logger.info(f"   appointment_id: {get_slot_value(tracker, 'conversation_id')}")
            logger.info(f"   start_time (pasado): {start_time}")
            logger.info(f"   end_time (pasado): {end_time}")
            
            # Validar parámetros requeridos
            required_params = [resource_id, service_id, start_time, end_time, patient_id]
            if not all(required_params):
                logger.error(f"Parámetros faltantes para get_slots_optimized: {required_params}")
                logger.error(f"   resource_id: {resource_id}")
                logger.error(f"   service_id: {service_id}")
                logger.error(f"   start_time: {start_time}")
                logger.error(f"   finish_time: {end_time}")
                logger.error(f"   patient_id: {patient_id}")
                return None
            
            # Convertir tipos
            adjacent_slots_int = int(adjacent_slots) if adjacent_slots else 1
            coverage_plan_id_str = str(coverage_plan_id) if coverage_plan_id else "1"
            
            logger.info(f"🔧 Llamando get_slots_optimized con parámetros:")
            logger.info(f"   resource_id: {resource_id}")
            logger.info(f"   service_id: {service_id}")
            logger.info(f"   coverage_plan_id: {coverage_plan_id_str}")
            logger.info(f"   start_time: {start_time}")
            logger.info(f"   finish_time: {end_time}")
            logger.info(f"   adjacent_slots: {adjacent_slots_int}")
            logger.info(f"   patient_id: {patient_id}")
            logger.info(f"   reschedule_appointment_id: {reschedule_appointment_id}")
            
            # Llamar a la función
            logger.info(f"📞 Invocando get_slots_optimized...")
            response = get_slots_optimized(
                resource_id=resource_id,
                service_id=service_id,
                coverage_plan_id=coverage_plan_id_str,
                start_time=start_time,
                finish_time=end_time,
                adjacent_slots=adjacent_slots_int,
                patient_id=patient_id,
                reschedule_appointment_id=reschedule_appointment_id
            )
            
            if response:
                logger.info(f"✅ get_slots_optimized retornó datos exitosamente")
            else:
                logger.warning(f"⚠️ get_slots_optimized retornó None")
            
            return response
            
        except Exception as e:
            logger.error(f"Error llamando get_slots_optimized: {e}")
            return None

    def _call_get_slots_optimized(self, tracker: Tracker) -> Dict:
        """
        Llama a la función get_slots_optimized con los parámetros de los slots.
        
        Args:
            tracker: Tracker de RASA
            
        Returns:
            Dict: Respuesta de la API o None si hay error
        """
        try:
            # Obtener parámetros de los slots
            resource_id = get_slot_value(tracker, "resource_id") or get_slot_value(tracker, "resource_name")
            service_id = get_slot_value(tracker, "id_especialidad")
            coverage_plan_id = get_slot_value(tracker, "autopago", "1")  # Default a 1 si no existe
            start_time = get_slot_value(tracker, "start_time")
            end_time = get_slot_value(tracker, "end_time")
            adjacent_slots = get_slot_value(tracker, "adjacent_slots", "1")  # Default a 1
            patient_id = get_slot_value(tracker, "patient_id")  # Usar el slot patient_id correcto
            reschedule_appointment_id = get_slot_value(tracker, "conversation_id")
            
            # Log de todos los slots para debugging
            logger.info(f"🔍 Debugging slots:")
            logger.info(f"   resource_id: {get_slot_value(tracker, 'resource_id')}")
            logger.info(f"   id_especialidad: {get_slot_value(tracker, 'id_especialidad')}")
            logger.info(f"   autopago: {get_slot_value(tracker, 'autopago')}")
            logger.info(f"   start_time: {get_slot_value(tracker, 'start_time')}")
            logger.info(f"   end_time: {get_slot_value(tracker, 'end_time')}")
            logger.info(f"   phone_number: {get_slot_value(tracker, 'phone_number')}")
            logger.info(f"   appointment_id: {get_slot_value(tracker, 'appointment_id')}")
            
            # Validar parámetros requeridos
            required_params = [resource_id, service_id, start_time, end_time, patient_id]
            if not all(required_params):
                logger.error(f"Parámetros faltantes para get_slots_optimized: {required_params}")
                logger.error(f"   resource_id: {resource_id}")
                logger.error(f"   service_id: {service_id}")
                logger.error(f"   start_time: {start_time}")
                logger.error(f"   finish_time: {end_time}")
                logger.error(f"   patient_id: {patient_id}")
                return None
            
            # Convertir tipos
            adjacent_slots_int = int(adjacent_slots) if adjacent_slots else 1
            coverage_plan_id_str = str(coverage_plan_id) if coverage_plan_id else "1"
            
            logger.info(f"🔧 Llamando get_slots_optimized con parámetros:")
            logger.info(f"   resource_id: {resource_id}")
            logger.info(f"   service_id: {service_id}")
            logger.info(f"   coverage_plan_id: {coverage_plan_id_str}")
            logger.info(f"   start_time: {start_time}")
            logger.info(f"   finish_time: {end_time}")
            logger.info(f"   adjacent_slots: {adjacent_slots_int}")
            logger.info(f"   patient_id: {patient_id}")
            logger.info(f"   reschedule_appointment_id: {reschedule_appointment_id}")
            
            # Llamar a la función
            logger.info(f"📞 Invocando get_slots_optimized...")
            response = get_slots_optimized(
                resource_id=resource_id,
                service_id=service_id,
                coverage_plan_id=coverage_plan_id_str,
                start_time=start_time,
                finish_time=end_time,
                adjacent_slots=adjacent_slots_int,
                patient_id=patient_id,
                reschedule_appointment_id=reschedule_appointment_id
            )
            
            if response:
                logger.info(f"✅ get_slots_optimized retornó datos exitosamente")
            else:
                logger.warning(f"⚠️ get_slots_optimized retornó None")
            
            return response
            
        except Exception as e:
            logger.error(f"Error llamando get_slots_optimized: {e}")
            return None


class ActionShowAvailableSlots(Action):
    """
    Acción para mostrar las opciones de horarios disponibles al usuario.
    Genera una respuesta JSON con estructura de lista interactiva de WhatsApp.
    """
    
    def name(self) -> Text:
        return "action_show_available_slots"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener la respuesta original de slots de la API
            slots_response = get_slot_value(tracker, "slots_response")
            
            if not slots_response or "slots" not in slots_response:
                dispatcher.utter_message(text="❌ No hay horarios disponibles en este momento.")
                return []
            
            # Filtrar slots disponibles (Bookable = true) y tomar los primeros 5
            available_slots = []
            for slot in slots_response["slots"]:
                if slot.get("Bookable", {}).get("Bookable", False):
                    available_slots.append(slot)
                    if len(available_slots) >= 5:  # Limitar a 5 opciones
                        break
            
            if not available_slots:
                dispatcher.utter_message(text="❌ No hay horarios disponibles en este momento.")
                return []
            
            # Generar las filas de la lista
            rows = []
            for i, slot in enumerate(available_slots, 1):
                timestamp = slot.get("Timestamp")
                if timestamp:
                    # Convertir timestamp Unix a datetime en zona horaria de Chile
                    from datetime import datetime
                    import pytz
                    
                    # Crear datetime en UTC
                    dt_utc = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
                    
                    # Convertir a zona horaria de Chile
                    chile_tz = pytz.timezone('America/Santiago')
                    dt_chile = dt_utc.astimezone(chile_tz)
                    
                    # Formatear fecha y hora
                    title = self._format_date_spanish(dt_chile)
                    description = dt_chile.strftime("%H:%M")
                    
                    rows.append({
                        "id": "cita_fecha_" + str(i),
                        "title": title,
                        "description": description
                    })
            
            # Agregar opción "Ninguna" al final
            rows.append({
                "id": "cita_fecha_" + str(len(rows) + 1),
                "title": "Ninguna"
            })
            
            # Construir la respuesta JSON
            response_json = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                        "text": "¡Perfecto! 😊 Estas son las opciones más cercanas disponibles:"
                    },
                    "footer": {
                        "text": "¿Cuál de estas fechas le acomoda más?"
                    },
                    "action": {
                        "button": "Fechas disponibles",
                        "sections": [
                            {
                                "rows": rows
                            }
                        ]
                    }
                }
            }
            
            # Enviar la respuesta JSON
            dispatcher.utter_message(json_message=response_json)
            
            logger.info(f"Lista interactiva enviada con {len(rows)} opciones")
            return [SlotSet("citas_disponibles", available_slots)]
            
        except Exception as e:
            error_message = f"Error mostrando slots disponibles: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            dispatcher.utter_message(text="❌ Error mostrando los horarios disponibles.")
            return []
    
    def _format_date_spanish(self, dt: datetime) -> str:
        """
        Formatea una fecha en formato español sin año.
        
        Args:
            dt: Objeto datetime en zona horaria de Chile
            
        Returns:
            str: Fecha formateada como "jueves 10 de julio"
        """
        try:
            # Nombres de los días de la semana
            dias_semana = {
                0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
                4: "viernes", 5: "sábado", 6: "domingo"
            }
            
            # Nombres de los meses
            meses = {
                1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
                5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
                9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
            }
            
            dia_semana = dias_semana[dt.weekday()]
            dia = dt.day
            mes = meses[dt.month]
            
            return f"{dia_semana} {dia} de {mes}"
            
        except Exception as e:
            logger.error(f"Error formateando fecha: {e}")
            return dt.strftime("%A %d de %B")  # Fallback


class ActionProcessSlotSelection(Action):
    """
    Acción para procesar la selección de horario del usuario.
    """
    def get_token(self) -> str:
        url = "https://redsalud-qa.apigee.net/redsaludauth/oauth/accesstoken"
        headers = {
            "Authorization": "Basic NHR1MFlQcHVkUG1SRTJidmd5aGVEYktuVkFtUGRDcUs6aUhWTm4wR1pVMEtKMmlOOA==",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-API-Key": "bloqueos"
        }
        data = {"grant_type": "client_credentials"}
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json().get("access_token")
        except Exception as e:
            print(f"Error obteniendo token: {e}")
            return None

    def create_appointment(self, token: str, payload: Dict) -> Dict:
        url = "https://redsalud-qa.apigee.net/agendarsv2/cita/AppointmentCreate/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-apikey": "bloqueos"
        }
        try:
            # Generar comando curl para logging
            curl_command = f'curl -X POST "{url}" \\\n'
            curl_command += ' \\\n'.join([f'  -H "{k}: {v}"' for k, v in headers.items()])
            curl_command += f' \\\n  -d \'{json.dumps(payload, indent=2)}\''
            print("[CURL COMMAND]", curl_command)
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creando cita: {e}")
            return None
        
    def name(self) -> Text:
        return "action_process_slot_selection"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtener el intent del último mensaje
        current_intent = tracker.latest_message.get('intent', {}).get('name')
        
        # Verificar si es el intent de seleccionar cita nueva fecha
        if current_intent == "seleccionar_cita_nueva_fecha":
            # Obtener el texto del mensaje para extraer el número de opción
            user_message = tracker.latest_message.get('text', '').lower()
            logger.info(f"Procesando selección de cita: {user_message}")
            
            # Extraer el número de la opción seleccionada (cita_fecha_1, cita_fecha_2, etc.)
            opcion_seleccionada = self._extract_option_number(user_message)
            logger.info(f"Opción extraída: {opcion_seleccionada}")
            
            slots_disponibles = tracker.get_slot("citas_disponibles")
            if opcion_seleccionada is not None and slots_disponibles is not None:
                try:
                    idx = int(opcion_seleccionada) - 1
                    if 0 <= idx < len(slots_disponibles):
                        fecha_confirmada = slots_disponibles[idx]
                        # Obtener token
                        token = self.get_token()
                        if token:
                            # Obtener valores de los slots
                            service_id = tracker.get_slot("service_id")
                            resource_id = tracker.get_slot("resource_id")
                            center_id = tracker.get_slot("id_centro_medico")
                            patient_id = tracker.get_slot("patient_id")
                            coverage_plan_id = tracker.get_slot("coverage_plan_id")
                            conversation_id = tracker.get_slot("conversation_id")
                            appointment_type_id = tracker.get_slot("appointment_type_id")
                        
                            # Formatear fecha_confirmada a formato ISO
                            print("DEBUG - Fecha confirmada: ", fecha_confirmada)
                            try:
                                # Extraer timestamp del slot (fecha_confirmada es un diccionario)
                                if isinstance(fecha_confirmada, dict) and 'Timestamp' in fecha_confirmada:
                                    timestamp = fecha_confirmada['Timestamp']
                                    # Convertir timestamp Unix a datetime
                                    dt = datetime.fromtimestamp(timestamp)
                                    datetime_from = dt.strftime("%Y-%m-%dT%H:%M:00")
                                    print(f"DEBUG - Timestamp extraído: {timestamp}")
                                    print(f"DEBUG - DateTime convertido: {datetime_from}")
                                else:
                                    # Fallback si no es un diccionario o no tiene timestamp
                                    print("DEBUG - fecha_confirmada no es un diccionario válido, usando valor por defecto")
                                    datetime_from = "2025-04-25T10:00:00"
                            except (ValueError, TypeError) as e:
                                print(f"DEBUG - Error procesando fecha: {e}")
                                datetime_from = "2025-04-25T10:00:00"  # Valor por defecto si hay error
                            # Preparar payload para crear cita
                            payload = {
                                "Service": {"Id": service_id},
                                "Resource": {"Id": resource_id},
                                "Center": {"Id": center_id},
                                "Patient": {"Id": patient_id},
                                "CoveragePlan": {"Id": coverage_plan_id},
                                "DateTimeFrom": datetime_from,
                                "Duration": 30,
                                "Status": "Booked",
                                "IsOvercapacity": False,
                                "NumberOfSlots": 1,
                                "AppointmentTypeId": appointment_type_id,
                                "RescheduleAppointmentId": conversation_id
                            }
                            print("DEBUG - Payload: ", payload)
                                                        # Crear cita
                            result = self.create_appointment(token, payload)
                            print("DEBUG - Creating appointment: ", result)
                            
                            # Actualizar estado en la base de datos según el resultado
                            try:
                                from .database import DatabaseConnection
                                db = DatabaseConnection()
                                
                                if result:
                                    # Éxito: actualizar estado a "rebooking success"
                                    success = db.update_appointment_status(conversation_id, "rebooking success")
                                    if success:
                                        logger.info(f"Estado de cita {conversation_id} actualizado a 'rebooking success'")
                                    else:
                                        logger.warning(f"No se pudo actualizar el estado de la cita {conversation_id}")
                                    
                                    print(f"Cita creada: {result}")
                                    dispatcher.utter_message(response="utter_waiting_for_confirmation")
                                    dispatcher.utter_message(response="utter_rebooking_success")
                                    return [SlotSet("fecha_seleccionada_confirmada", fecha_confirmada)]
                                else:
                                    # Fallo: actualizar estado a "rebooking failed"
                                    success = db.update_appointment_status(conversation_id, "rebooking failed")
                                    if success:
                                        logger.info(f"Estado de cita {conversation_id} actualizado a 'rebooking failed'")
                                    else:
                                        logger.warning(f"No se pudo actualizar el estado de la cita {conversation_id}")
                                    
                                    print("DEBUG - Error al crear cita")
                                    dispatcher.utter_message(response="utter_waiting_for_confirmation")
                                    dispatcher.utter_message(response="utter_rebookig_booking_error")
                                    return [SlotSet("fecha_seleccionada_confirmada", "Ninguna")]
                                    
                            except Exception as e:
                                logger.error(f"Error actualizando estado en base de datos: {str(e)}")
                                # Continuar con el flujo normal incluso si falla la actualización de BD
                                if result:
                                    print(f"Cita creada: {result}")
                                    dispatcher.utter_message(response="utter_waiting_for_confirmation")
                                    dispatcher.utter_message(response="utter_rebooking_success")
                                    return [SlotSet("fecha_seleccionada_confirmada", fecha_confirmada)]
                                else:
                                    print("DEBUG - Error al crear cita")
                                    dispatcher.utter_message(response="utter_waiting_for_confirmation")
                                    dispatcher.utter_message(response="utter_rebookig_booking_error")
                                    return [SlotSet("fecha_seleccionada_confirmada", "Ninguna")]

                        else:
                            # Error al obtener token
                            logger.error("No se pudo obtener el token de autenticación")
                            dispatcher.utter_message(response="utter_waiting_for_confirmation")
                            dispatcher.utter_message(response="utter_rebooking_booking_error")
                            return [SlotSet("fecha_seleccionada_confirmada", "Ninguna")]
                            
                except (ValueError, IndexError):
                    pass
        else:
            logger.warning(f"Intent no reconocido o datos faltantes: {current_intent}")
            dispatcher.utter_message(text="❌ No se pudo procesar tu selección. Por favor, intenta de nuevo.")
        
        return []
    
    def _extract_option_number(self, message: str) -> Optional[int]:
        """
        Extrae el número de opción del mensaje del usuario.
        
        Args:
            message: Mensaje del usuario (ej: "cita_fecha_1", "cita_fecha_2", etc.)
            
        Returns:
            int: Número de la opción (1, 2, 3, etc.) o None si no se puede extraer
        """
        try:
            import re
            
            # Buscar patrones como "cita_fecha_1", "cita_fecha_2", etc.
            pattern = r'cita_fecha_(\d+)'
            match = re.search(pattern, message.lower())
            
            if match:
                option_number = int(match.group(1))
                logger.info(f"Opción extraída del mensaje '{message}': {option_number}")
                return option_number
            
            # Si no encuentra el patrón, buscar solo números
            number_pattern = r'(\d+)'
            match = re.search(number_pattern, message)
            
            if match:
                option_number = int(match.group(1))
                logger.info(f"Número extraído del mensaje '{message}': {option_number}")
                return option_number
            
            logger.warning(f"No se pudo extraer número de opción del mensaje: {message}")
            return None
            
        except Exception as e:
            logger.error(f"Error extrayendo número de opción: {e}")
            return None


class ActionConfirmRebooking(Action):
    """
    Acción para confirmar el rebooking de la cita.
    """
    
    def name(self) -> Text:
        return "action_confirm_rebooking"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener información de la cita
            selected_slot = get_slot_value(tracker, "selected_slot")
            appointment_id = get_slot_value(tracker, "appointment_id")
            nombre_paciente = get_slot_value(tracker, "nombre_paciente")
            especialidad = get_slot_value(tracker, "especialidad")
            centro_medico = get_slot_value(tracker, "centro_medico")
            
            if not all([selected_slot, appointment_id]):
                dispatcher.utter_message(text="❌ Error: Información incompleta para confirmar el rebooking.")
                return []
            
            # Aquí se haría la llamada a la API para confirmar el rebooking
            # Por ahora, simulamos la confirmación
            
            success_message = f"""✅ **¡Reagendamiento confirmado!**

📋 **Detalles de tu nueva cita:**
• **Paciente:** {nombre_paciente}
• **Especialidad:** {especialidad}
• **Centro médico:** {centro_medico}
• **Nuevo horario:** {selected_slot}

Tu cita ha sido reagendada exitosamente. Recibirás una confirmación por WhatsApp.

¿Hay algo más en lo que pueda ayudarte?"""
            
            dispatcher.utter_message(text=success_message)
            
            # Limpiar slots de rebooking
            cleanup_events = [
                SlotSet("contexto_rebooking", None),
                SlotSet("rebooking_fecha", None),
                SlotSet("rebooking_hora", None),
                SlotSet("start_time", None),
                SlotSet("end_time", None),
                SlotSet("available_slots", None),
                SlotSet("selected_slot", None),
                SlotSet("slot_selection_index", None)
            ]
            
            return cleanup_events
            
        except Exception as e:
            error_message = f"Error confirmando rebooking: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            dispatcher.utter_message(text="❌ Error confirmando el reagendamiento. Por favor, intenta de nuevo.")
            return []


class ActionCancelRebooking(Action):
    """
    Acción para cancelar el proceso de rebooking.
    """
    
    def name(self) -> Text:
        return "action_cancel_rebooking"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Mensaje de cancelación
            cancel_message = """❌ **Reagendamiento cancelado**

Tu cita original se mantiene sin cambios. Si necesitas reagendar en otro momento, puedes volver a solicitarlo.

¿Hay algo más en lo que pueda ayudarte?"""
            
            dispatcher.utter_message(text=cancel_message)
            
            # Limpiar slots de rebooking
            cleanup_events = [
                SlotSet("contexto_rebooking", None),
                SlotSet("rebooking_fecha", None),
                SlotSet("rebooking_hora", None),
                SlotSet("start_time", None),
                SlotSet("end_time", None),
                SlotSet("available_slots", None),
                SlotSet("selected_slot", None),
                SlotSet("slot_selection_index", None)
            ]
            
            return cleanup_events
            
        except Exception as e:
            error_message = f"Error cancelando rebooking: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            dispatcher.utter_message(text="❌ Error cancelando el reagendamiento.")
            return [] 


class ActionHandleRebookingDenial(Action):
    """
    Acción para manejar la negación del rebooking.
    Establece los slots apropiados y actualiza el estado en la base de datos.
    """
    
    def name(self) -> Text:
        return "action_handle_rebooking_denial"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log_request_info(tracker, self.name())
        
        try:
            # Obtener appointment_id del tracker
            appointment_id = get_slot_value(tracker, "appointment_id")
            
            # Actualizar estado en la base de datos
            if appointment_id:
                try:
                    from .database import DatabaseConnection
                    db = DatabaseConnection()
                    
                    # Actualizar estado a "rebooking reject"
                    success = db.update_appointment_status(appointment_id, "rebooking reject")
                    
                    if success:
                        logger.info(f"Estado de cita {appointment_id} actualizado a 'rebooking reject'")
                    else:
                        logger.warning(f"No se pudo actualizar el estado de la cita {appointment_id}")
                        
                except Exception as e:
                    logger.error(f"Error actualizando estado en base de datos: {str(e)}")
            else:
                logger.warning("No se encontró appointment_id para actualizar estado")
            
            # Establecer los slots según los requerimientos
            slot_events = []
            
            logger.info("Slots actualizados: contexto=None, contexto_rebooking=None, contexto_rebooking_menu=activado")
            
            # Agregar followup action para inicializar el menú de rebooking
            slot_events.append(FollowupAction("action_init_rebooking_menu"))
            logger.info("Followup action agregado: action_init_rebooking_menu")
            
            return slot_events
            
        except Exception as e:
            error_message = f"Error manejando negación de rebooking: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            # Aún intentar limpiar los slots en caso de error y agregar followup
            return [
                SlotSet("contexto", None),
                SlotSet("contexto_rebooking", None),
                SlotSet("contexto_rebooking_menu", "activado"),
                FollowupAction("action_init_rebooking_menu")
            ]