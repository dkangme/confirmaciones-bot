#!/usr/bin/env python3
"""
Aplicación para generar JSON de rebooking a partir de appointment_id.
Conecta a la base de datos PostgreSQL y genera el JSON requerido para EXTERNAL_init_rebooking.
"""

import os
import sys
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AppointmentJSONGenerator:
    """
    Clase para generar JSON de rebooking a partir de appointment_id.
    """
    
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.connection_params = {
            'host': os.getenv('DB_HOST', '34.45.109.62'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'bot'),
            'user': os.getenv('DB_USER', 'bot_client'),
            'password': os.getenv('DB_PASSWORD', 'Cg:m8mY=xZR?LB#*')
        }
    
    def get_appointment_by_id(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un registro de appointment por su ID.
        
        Args:
            appointment_id: ID único de la cita
            
        Returns:
            Diccionario con los datos de la cita o None si no se encuentra
        """
        try:
            conn = psycopg2.connect(**self.connection_params)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT * FROM appointments 
                    WHERE appointment_id = %s
                """
                cur.execute(query, (appointment_id,))
                result = cur.fetchone()
                
                if result:
                    logger.info(f"Registro encontrado para appointment_id: {appointment_id}")
                    return dict(result)
                else:
                    logger.warning(f"No se encontró registro para appointment_id: {appointment_id}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error obteniendo appointment: {str(e)}")
            return None
        finally:
            if conn:
                conn.close()
    
    def generate_rebooking_json(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera el JSON de rebooking a partir de los datos de la cita.
        
        Args:
            appointment_data: Datos de la cita obtenidos de la base de datos
            
        Returns:
            JSON estructurado para EXTERNAL_init_rebooking
        """
        try:
            # Mapear campos de la BD a las entidades requeridas
            json_data = {
                "name": "EXTERNAL_init_rebooking",
                "entities": {
                    # Datos existentes (mapeados desde la BD)
                    "nombre_paciente": appointment_data.get('patient_full_name', ''),
                    "id_especialidad": appointment_data.get('service_specialty_id', ''),
                    "especialidad": appointment_data.get('service_specialty_name', ''),
                    "fecha_hora": appointment_data.get('date_time_from', ''),
                    "id_centro_medico": appointment_data.get('center_id', ''),
                    "centro_medico": appointment_data.get('center_name', ''),
                    "centro_medico_address": "",  # No disponible en BD actual
                    "centro_medico_google": "",   # No disponible en BD actual
                    "centro_medico_comuna": "",   # No disponible en BD actual
                    "area_medica": appointment_data.get('service_area_name', ''),
                    "bot_name": "Ricardo",
                    "campaign_name": "confirmacion",
                    "phone_number": appointment_data.get('patient_main_phone_number', ''),
                    "preparations": False,
                    "conversation_id": appointment_data.get('appointment_id', ''),
                    "preparations_url": "https://www.google.cl",
                    "preparation_pdf_name": "prepararions.pdf",
                    "resource_name": appointment_data.get('resource_name', ''),
                    "resource_id": appointment_data.get('resource_id', ''),
                    
                    # DATOS CRÍTICOS (mapeados desde la BD)
                    "patient_id": appointment_data.get('patient_id', ''),
                    "service_id": appointment_data.get('service_id', ''),
                    "coverage_plan_id": appointment_data.get('coverage_plan_id', ''),
                    "starting_location_id": appointment_data.get('center_id', ''),  # Usar center_id como starting_location_id
                    "original_appointment_id": appointment_data.get('appointment_id', ''),
                    "maximum_distance": 5,
                    "adjacent_slots": 1,
                    "app_timezone": -240,
                    "include_self_payer": False,
                    "expert_booking_mode": False,
                    "include_not_bookable": True,
                    "reschedule_appointment_id": appointment_data.get('appointment_id', '')
                }
            }
            
            logger.info("JSON de rebooking generado exitosamente")
            return json_data
            
        except Exception as e:
            logger.error(f"Error generando JSON: {str(e)}")
            return {}
    
    def process_appointment_id(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        """
        Procesa un appointment_id y genera el JSON de rebooking.
        
        Args:
            appointment_id: ID único de la cita
            
        Returns:
            JSON de rebooking o None si hay error
        """
        try:
            # Obtener datos de la cita
            appointment_data = self.get_appointment_by_id(appointment_id)
            
            if not appointment_data:
                logger.error(f"No se pudo obtener datos para appointment_id: {appointment_id}")
                return None
            
            # Generar JSON de rebooking
            rebooking_json = self.generate_rebooking_json(appointment_data)
            
            if not rebooking_json:
                logger.error("No se pudo generar JSON de rebooking")
                return None
            
            return rebooking_json
            
        except Exception as e:
            logger.error(f"Error procesando appointment_id {appointment_id}: {str(e)}")
            return None


def main():
    """
    Función principal de la aplicación.
    """
    if len(sys.argv) != 2:
        print("Uso: python appointment_json_generator.py <appointment_id>")
        print("Ejemplo: python appointment_json_generator.py 44191913-9766-4848-a195-b31001310d93")
        sys.exit(1)
    
    appointment_id = sys.argv[1]
    
    # Crear instancia del generador
    generator = AppointmentJSONGenerator()
    
    # Procesar appointment_id
    result = generator.process_appointment_id(appointment_id)
    
    if result:
        # Imprimir JSON formateado
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Error: No se pudo generar JSON para appointment_id: {appointment_id}")
        sys.exit(1)


if __name__ == "__main__":
    main() 