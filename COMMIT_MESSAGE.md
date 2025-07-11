feat: Mejorar reconocimiento de intent reagendamiento_menu_opcion5

- Agregar ejemplo de entrenamiento "reagendamiento_menu_opcion5" al intent reagendamiento_menu_opcion5
- Reentrenar modelo Rasa para mejorar reconocimiento de intents
- Solucionar problema de NLU fallback al enviar mensajes con formato específico
- Mantener compatibilidad con diferentes formatos de entrada para opción 5 del menú

Cambios técnicos:
- Actualizado data/nlu.yml con nuevo ejemplo de entrenamiento
- Modelo reentrenado exitosamente
- Servidor Rasa reiniciado con nuevo modelo

El bot ahora reconoce correctamente el mensaje "reagendamiento_menu_opcion_5" 
y responde apropiadamente con utter_show_rebooking_menu según las reglas configuradas. 