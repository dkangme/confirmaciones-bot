"""
Módulo para manejo de conexiones a PostgreSQL.
Proporciona una interfaz limpia para operaciones de base de datos.
"""

import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Clase para manejo de conexiones a PostgreSQL.
    Implementa pool de conexiones para mejor rendimiento.
    """
    
    def __init__(self):
        """Inicializa la configuración de conexión a la base de datos."""
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'bot_confirmaciones'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password')
        }
        
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Inicializa el pool de conexiones."""
        try:
            self.pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                **self.connection_params
            )
            logger.info("Pool de conexiones PostgreSQL inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar pool de conexiones: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SELECT y retorna los resultados.
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)
            
        Returns:
            Lista de diccionarios con los resultados
            
        Raises:
            Exception: Si hay error en la consulta
        """
        try:
            conn = self.pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                logger.debug(f"Ejecutando consulta: {query}")
                cur.execute(query, params)
                results = cur.fetchall()
                logger.debug(f"Consulta ejecutada exitosamente. Filas retornadas: {len(results)}")
                return [dict(row) for row in results], True
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {str(e)}")
            return [], False
        finally:
            if conn:
                self.pool.putconn(conn)
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """
        Ejecuta un comando INSERT, UPDATE, DELETE y retorna el número de filas afectadas.
        
        Args:
            command: Comando SQL a ejecutar
            params: Parámetros para el comando (opcional)
            
        Returns:
            Número de filas afectadas
            
        Raises:
            Exception: Si hay error en el comando
        """
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cur:
                logger.debug(f"Ejecutando comando: {command}")
                cur.execute(command, params)
                rows_affected = cur.rowcount
                conn.commit()
                logger.debug(f"Comando ejecutado exitosamente. Filas afectadas: {rows_affected}")
                return rows_affected
        except Exception as e:
            logger.error(f"Error ejecutando comando: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.pool.putconn(conn)
    
    def execute_transaction(self, commands: List[tuple]) -> bool:
        """
        Ejecuta múltiples comandos en una transacción.
        
        Args:
            commands: Lista de tuplas (comando, parámetros)
            
        Returns:
            True si la transacción fue exitosa, False en caso contrario
        """
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cur:
                for command, params in commands:
                    logger.debug(f"Ejecutando comando en transacción: {command}")
                    cur.execute(command, params)
                
                conn.commit()
                logger.info("Transacción ejecutada exitosamente")
                return True
        except Exception as e:
            logger.error(f"Error en transacción: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                self.pool.putconn(conn)
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos.
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                logger.info("Conexión a PostgreSQL probada exitosamente")
                return result[0] == 1
        except Exception as e:
            logger.error(f"Error probando conexión: {str(e)}")
            return False
        finally:
            if conn:
                self.pool.putconn(conn)
    
    def close_pool(self):
        """Cierra el pool de conexiones."""
        if self.pool:
            self.pool.closeall()
            logger.info("Pool de conexiones cerrado")
    
    def update_appointment_status(self, appointment_id: str, new_status: str) -> bool:
        """
        Actualiza el estado de una cita en la tabla appointments.
        También actualiza last_notification_date y updated_at con la fecha actual.
        
        Args:
            appointment_id: ID único de la cita
            status: Nuevo estado de la cita
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        try:
            query = """
                UPDATE appointments 
                SET status = %s, 
                    last_notification_date = NOW(), 
                    updated_at = NOW()
                WHERE appointment_id = %s
            """
            params = (new_status, appointment_id)
            
            rows_affected = self.execute_command(query, params)
            
            if rows_affected > 0:
                logger.info(f"Estado de cita {appointment_id} actualizado a '{new_status}' exitosamente")
                return True
            else:
                logger.warning(f"No se encontró la cita {appointment_id} para actualizar estado")
                return False
                
        except Exception as e:
            logger.error(f"Error actualizando estado de cita {appointment_id}: {str(e)}")
            return False

    def get_patient_phone_from_db(self, appointment_id):
        """
        Obtiene el número de teléfono del paciente desde la base de datos usando el appointment_id.

        Args:
            appointment_id: ID de la cita
            db_config: Configuración de la base de datos (opcional)

        Returns:
            str: Número de teléfono del paciente o None si no se encuentra
        """
        query = """
            SELECT patient_main_phone_number
            FROM appointments
            WHERE appointment_id = %s
        """
        result, success = self.execute_query(query, (appointment_id,))
        
        if success and result:
            logging.info(f"Resultado de la consulta: {result}")
            phone_number = result[0]['patient_main_phone_number']
            logging.info(f"Teléfono encontrado para appointment {appointment_id}: {phone_number}")
            return phone_number
        else:
            logging.error(f"No se encontró teléfono para appointment {appointment_id}")
            return None
        
# Instancia global para uso en actions
db_connection = DatabaseConnection() 