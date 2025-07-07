"""
Configuración de logging para el bot de confirmaciones.
Proporciona logging estructurado y configurable.
"""

import os
import logging
import colorlog
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def setup_logging():
    """
    Configura el sistema de logging para el bot.
    Establece formato, niveles y handlers.
    """
    
    # Obtener configuración de logging desde variables de entorno
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_file = os.getenv('LOG_FILE', 'bot_confirmaciones.log')
    
    # Crear directorio de logs si no existe
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar nivel de logging
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    # Configurar formato para consola (con colores)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    # Configurar formato para archivo
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configurar handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(console_formatter)
    
    # Configurar handler para archivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(file_formatter)
    
    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Limpiar handlers existentes
    root_logger.handlers.clear()
    
    # Agregar handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Configurar loggers específicos
    loggers_to_configure = [
        'rasa',
        'rasa_sdk',
        'actions',
        'database',
        'utils'
    ]
    
    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.setLevel(numeric_level)
        logger.propagate = True
    
    # Log inicial
    logging.info(f"Logging configurado - Nivel: {log_level}, Archivo: {log_file}")
    logging.info("Bot de confirmaciones iniciando...")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el módulo especificado.
    
    Args:
        name: Nombre del módulo/logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


# Configurar logging al importar el módulo
setup_logging() 