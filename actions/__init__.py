"""
Módulo de acciones personalizadas para el bot de confirmaciones.
"""

import logging

# Importar configuración de logging
import logging_config

# Importar módulos principales
from . import database
from . import utils
from . import actions
from . import rebooking_actions

# Importar acciones específicas
from .actions import (
    ActionInitContext,
    ActionFormatDate,
    ActionCancelAppointment,
    ActionConfirmAppointment,
    ActionFallback
)

# Importar acciones de rebooking
from .rebooking_actions import (
    ActionInitRebooking,
    ActionProcessDateRequest,
    ActionShowAvailableSlots,
    ActionProcessSlotSelection,
    ActionConfirmRebooking,
    ActionCancelRebooking
)

# Configurar logger para el módulo actions
logger = logging.getLogger(__name__)
logger.info("Módulo de acciones cargado correctamente")
