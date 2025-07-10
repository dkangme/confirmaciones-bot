"""
Módulo de acciones para el menú de reagendamiento.
Implementa la lógica para manejar el flujo del menú de reagendamiento.
"""

import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Configurar logger
logger = logging.getLogger(__name__)


class ActionInitRebookingMenu(Action):
    """
    Acción para inicializar el contexto del menú de reagendamiento.
    Configura los slots necesarios para el flujo del menú.
    """
    
    def name(self) -> Text:
        return "action_init_rebooking_menu"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        logger.info(f"Iniciando action_init_rebooking_menu para usuario: {tracker.sender_id}")
        
        try:
            # Configurar slots para el menú de reagendamiento
            slot_events = [
                SlotSet("contexto", None),
                SlotSet("contexto_rebooking", None),
                SlotSet("contexto_rebooking_menu", "activado")
            ]
            
            logger.info("Slots configurados para menú de reagendamiento:")
            logger.info("- contexto: None")
            logger.info("- contexto_rebooking: None")
            logger.info("- contexto_rebooking_menu: activado")
            
            # Mensaje de confirmación
            confirmation_message = """
✅ **Menú de Reagendamiento Inicializado**

🔄 **Contexto Configurado:**
• Contexto general: Desactivado
• Contexto rebooking: Desactivado
• Contexto menú rebooking: Activado

🎯 **Sistema listo para menú de reagendamiento**
            """.strip()
            
            dispatcher.utter_message(text=confirmation_message)
            
            logger.info(f"Menú de reagendamiento inicializado exitosamente para usuario: {tracker.sender_id}")
            
            return slot_events
            
        except Exception as e:
            error_message = f"Error inicializando menú de reagendamiento: {str(e)}"
            logger.error(error_message, exc_info=True)
            
            dispatcher.utter_message(text="❌ Error inicializando el menú de reagendamiento")
            
            return [] 