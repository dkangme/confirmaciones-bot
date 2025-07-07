# Funcionalidad de Rebooking - Documentación

## Descripción
Este directorio contiene todos los archivos relacionados con la funcionalidad de rebooking (reagendamiento) de citas médicas, separados del código principal para mejorar la organización y mantenibilidad.

## Archivos Incluidos

### 1. `rebooking_stories.yml`
Contiene todas las historias de conversación relacionadas con rebooking:
- **external init rebooking**: Inicialización del contexto de rebooking
- **direct rebooking flow**: Flujo directo de rebooking
- **complete rebooking context flow**: Flujo completo con contexto
- **complete rebooking cancellation flow**: Flujo de cancelación de rebooking

### 2. `rebooking_rules.yml`
Contiene todas las reglas de comportamiento para rebooking:
- **Initialize rebooking**: Regla para inicializar rebooking
- **Handle direct rebooking intent**: Manejo de intent directo
- **Show rebooking options**: Mostrar opciones cuando el contexto está activo
- **Confirm rebooking**: Confirmar cuando el usuario afirma
- **Cancel rebooking**: Cancelar cuando el usuario niega

### 3. `rebooking_nlu.yml`
Contiene los datos de entrenamiento NLU para rebooking:
- **EXTERNAL_init_rebooking**: Intent para inicialización externa
- **rebooking**: Intent principal de rebooking con ejemplos expandidos

## Acciones Relacionadas

### `actions/rebooking_actions.py`
Contiene la clase `ActionInitRebooking` que:
- Inicializa el contexto de rebooking
- Procesa entidades y actualiza slots
- Configura el slot `contexto_rebooking`
- Formatea fechas para mostrar al usuario
- Proporciona confirmación detallada

## Flujos de Conversación

### 1. Inicialización Externa
```
EXTERNAL_init_rebooking → action_init_rebooking
```

### 2. Flujo Directo
```
rebooking → utter_rebooking
```

### 3. Flujo con Contexto
```
contexto_rebooking: "rebooking" + greet → utter_rebooking
contexto_rebooking: "rebooking" + affirm → utter_rebooking_confirmed
contexto_rebooking: "rebooking" + deny → utter_rebooking_cancelled
```

## Integración

### Archivos Principales que Referencian Rebooking:
- **domain.yml**: Define intents, slots y utterances de rebooking
- **actions/__init__.py**: Importa las acciones de rebooking
- **config.yml**: Configuración del pipeline (automático)

### Slots Utilizados:
- `contexto_rebooking`: Controla el flujo de rebooking
- `fecha_hora_formato`: Fecha formateada para mostrar
- Otros slots estándar (nombre_paciente, especialidad, etc.)

## Ventajas de la Separación

1. **Organización**: Código relacionado agrupado en archivos específicos
2. **Mantenibilidad**: Cambios en rebooking no afectan otras funcionalidades
3. **Escalabilidad**: Fácil agregar nuevas funcionalidades similares
4. **Testing**: Pruebas específicas para rebooking
5. **Documentación**: Documentación clara y específica

## Uso

Rasa automáticamente detecta y utiliza todos los archivos `.yml` en el directorio `data/`, por lo que no se requieren cambios adicionales en la configuración.

Para entrenar el modelo:
```bash
rasa train
```

Para probar específicamente rebooking:
```bash
rasa test --stories data/rebooking_stories.yml
``` 