"""
Módulo de utilidades compartidas para el bot de confirmaciones.
Proporciona funciones helper para validaciones, formateo y operaciones comunes.
"""

import os
import re
import json
import logging
from datetime import datetime, date
from typing import Dict, Any, Optional, List
from dateutil import parser
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    pass


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    Valida que los campos requeridos estén presentes y no sean vacíos.
    
    Args:
        data: Diccionario con los datos a validar
        required_fields: Lista de campos requeridos
        
    Returns:
        True si todos los campos están presentes y no son vacíos
        
    Raises:
        ValidationError: Si algún campo requerido falta o está vacío
    """
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Campo requerido '{field}' no encontrado")
        
        value = data[field]
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValidationError(f"Campo requerido '{field}' no puede estar vacío")
    
    return True


def validate_date_format(date_string: str, format_pattern: str = "%Y-%m-%d") -> bool:
    """
    Valida que una cadena de fecha tenga el formato correcto.
    
    Args:
        date_string: Cadena de fecha a validar
        format_pattern: Patrón de formato esperado
        
    Returns:
        True si la fecha tiene el formato correcto
        
    Raises:
        ValidationError: Si la fecha no tiene el formato correcto
    """
    try:
        datetime.strptime(date_string, format_pattern)
        return True
    except ValueError:
        raise ValidationError(f"Formato de fecha inválido. Se espera: {format_pattern}")


def validate_time_format(time_string: str, format_pattern: str = "%H:%M") -> bool:
    """
    Valida que una cadena de hora tenga el formato correcto.
    
    Args:
        time_string: Cadena de hora a validar
        format_pattern: Patrón de formato esperado
        
    Returns:
        True si la hora tiene el formato correcto
        
    Raises:
        ValidationError: Si la hora no tiene el formato correcto
    """
    try:
        datetime.strptime(time_string, format_pattern)
        return True
    except ValueError:
        raise ValidationError(f"Formato de hora inválido. Se espera: {format_pattern}")


def parse_date_string(date_string: str) -> Optional[date]:
    """
    Parsea una cadena de fecha a objeto date.
    
    Args:
        date_string: Cadena de fecha a parsear
        
    Returns:
        Objeto date o None si no se puede parsear
    """
    try:
        return parser.parse(date_string).date()
    except (ValueError, TypeError):
        logger.warning(f"No se pudo parsear la fecha: {date_string}")
        return None


def format_date_for_display(date_obj: date) -> str:
    """
    Formatea una fecha para mostrar al usuario.
    
    Args:
        date_obj: Objeto date a formatear
        
    Returns:
        Fecha formateada como string
    """
    return date_obj.strftime("%d/%m/%Y")


def format_time_for_display(time_string: str) -> str:
    """
    Formatea una hora para mostrar al usuario.
    
    Args:
        time_string: Hora en formato HH:MM
        
    Returns:
        Hora formateada como string
    """
    try:
        time_obj = datetime.strptime(time_string, "%H:%M")
        return time_obj.strftime("%I:%M %p")  # Formato 12 horas con AM/PM
    except ValueError:
        return time_string


def sanitize_string(input_string: str) -> str:
    """
    Sanitiza una cadena de texto removiendo caracteres peligrosos.
    
    Args:
        input_string: Cadena a sanitizar
        
    Returns:
        Cadena sanitizada
    """
    if not input_string:
        return ""
    
    # Remover caracteres de control y caracteres peligrosos para SQL
    sanitized = re.sub(r'[^\w\s\-.,@#$%&()]', '', input_string)
    return sanitized.strip()


def create_json_response(success: bool, message: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Crea una respuesta JSON estándar.
    
    Args:
        success: Indica si la operación fue exitosa
        message: Mensaje descriptivo
        data: Datos adicionales (opcional)
        
    Returns:
        Diccionario con la respuesta JSON
    """
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if data:
        response["data"] = data
    
    return response


def log_request_info(tracker, action_name: str):
    """
    Registra información de la request para debugging.
    
    Args:
        tracker: Tracker de RASA
        action_name: Nombre de la acción que se está ejecutando
    """
    logger.info(f"Ejecutando {action_name} para usuario: {tracker.sender_id}")
    logger.debug(f"Slots actuales: {tracker.current_state()['slots']}")
    logger.debug(f"Último mensaje: {tracker.latest_message}")


def get_slot_value(tracker, slot_name: str, default: Any = None) -> Any:
    """
    Obtiene el valor de un slot de forma segura.
    
    Args:
        tracker: Tracker de RASA
        slot_name: Nombre del slot
        default: Valor por defecto si el slot no existe
        
    Returns:
        Valor del slot o el valor por defecto
    """
    try:
        value = tracker.get_slot(slot_name)
        return value if value is not None else default
    except Exception as e:
        logger.warning(f"Error obteniendo slot '{slot_name}': {str(e)}")
        return default


def extract_entity_value(tracker, entity_name: str) -> Optional[str]:
    """
    Extrae el valor de una entidad del último mensaje.
    
    Args:
        tracker: Tracker de RASA
        entity_name: Nombre de la entidad
        
    Returns:
        Valor de la entidad o None si no se encuentra
    """
    try:
        entities = tracker.latest_message.get('entities', [])
        for entity in entities:
            if entity.get('entity') == entity_name:
                return entity.get('value')
        return None
    except Exception as e:
        logger.warning(f"Error extrayendo entidad '{entity_name}': {str(e)}")
        return None


def validate_email_format(email: str) -> bool:
    """
    Valida el formato de un email.
    
    Args:
        email: Email a validar
        
    Returns:
        True si el email tiene formato válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone_format(phone: str) -> bool:
    """
    Valida el formato de un número de teléfono.
    
    Args:
        phone: Número de teléfono a validar
        
    Returns:
        True si el teléfono tiene formato válido
    """
    # Patrón básico para números de teléfono (puede ajustarse según el país)
    pattern = r'^[\+]?[0-9\s\-\(\)]{7,15}$'
    return bool(re.match(pattern, phone))


def get_environment_variable(var_name: str, default: str = None) -> str:
    """
    Obtiene una variable de entorno de forma segura.
    
    Args:
        var_name: Nombre de la variable de entorno
        default: Valor por defecto si la variable no existe
        
    Returns:
        Valor de la variable de entorno o el valor por defecto
    """
    value = os.getenv(var_name, default)
    if value is None:
        logger.warning(f"Variable de entorno '{var_name}' no encontrada")
    return value


 