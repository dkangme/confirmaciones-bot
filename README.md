# Bot de Confirmaciones - RASA

Bot conversacional para manejo de confirmaciones de citas médicas desarrollado con RASA 3.6.21.

## 🚀 Características

- **Framework**: RASA 3.6.21 con Rasa SDK 3.6.2
- **Base de Datos**: PostgreSQL con pool de conexiones
- **Comunicación**: REST API
- **Logging**: Estructurado con colores y archivos
- **Validaciones**: Robustas con manejo de errores
- **Configuración**: Variables de entorno (.env)

## 📋 Prerrequisitos

- Python 3.8.10+
- PostgreSQL 12+
- pip

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd bot-confirmaciones
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Configuración de Base de Datos PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bot_confirmaciones
DB_USER=postgres
DB_PASSWORD=tu_password

# Configuración de APIs (se especificarán caso a caso)
API_KEY=
API_URL=

# Configuración de Logging
LOG_LEVEL=INFO
LOG_FILE=bot_confirmaciones.log

# Configuración de RASA
RASA_HOST=localhost
RASA_PORT=5005
RASA_ACTIONS_PORT=5055
```

## 🏃‍♂️ Ejecución

### 1. Entrenar el modelo
```bash
rasa train
```

### 2. Ejecutar el servidor de acciones (en una terminal)
```bash
rasa run actions
```

### 3. Ejecutar el servidor principal (en otra terminal)
```bash
rasa run --enable-api --cors "*"
```

### 4. Probar el bot
```bash
rasa shell
```

## 📁 Estructura del Proyecto

```
bot-confirmaciones/
├── actions/
│   ├── __init__.py
│   ├── actions.py          # Acciones personalizadas
│   ├── database.py         # Conexión a PostgreSQL
│   └── utils.py           # Utilidades compartidas
├── data/
│   ├── nlu.yml            # Datos de entrenamiento NLU
│   ├── stories.yml        # Historias de conversación
│   └── rules.yml          # Reglas del bot
├── models/                # Modelos entrenados
├── tests/                 # Tests del bot
├── config.yml             # Configuración del pipeline
├── domain.yml             # Definición del dominio
├── endpoints.yml          # Configuración de endpoints
├── credentials.yml        # Credenciales (REST channel)
├── requirements.txt       # Dependencias del proyecto
├── logging_config.py      # Configuración de logging
└── README.md             # Documentación
```

## 🔧 Configuración

### Base de Datos PostgreSQL

El bot utiliza PostgreSQL para almacenar información de citas. La conexión se maneja a través de la clase `DatabaseConnection` en `actions/database.py`.

**Características:**
- Pool de conexiones para mejor rendimiento
- Manejo automático de transacciones
- Logging detallado de operaciones
- Manejo robusto de errores

### Logging

El sistema de logging está configurado en `logging_config.py` con las siguientes características:

- **Consola**: Logs con colores para mejor legibilidad
- **Archivo**: Logs detallados con timestamps
- **Niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Configuración**: A través de variables de entorno

### Actions Personalizadas

Las acciones están implementadas en `actions/actions.py` siguiendo las mejores prácticas:

- **Logging**: Cada acción registra su ejecución
- **Manejo de errores**: Try-catch con respuestas amigables
- **Validaciones**: Entrada de datos validada y sanitizada
- **Modularidad**: Código organizado y reutilizable

## 🧪 Testing

### Probar conexión a base de datos
```bash
rasa shell
# En el chat: "probar conexión"
```

### Verificar estado del sistema
```bash
rasa shell
# En el chat: "estado del sistema"
```

## 📝 Desarrollo

### Agregar nuevas acciones

1. Crear la clase en `actions/actions.py`
2. Implementar métodos `name()` y `run()`
3. Agregar logging y manejo de errores
4. Registrar en `domain.yml`

### Agregar nuevos intents

1. Definir en `data/nlu.yml`
2. Agregar ejemplos de entrenamiento
3. Crear historias en `data/stories.yml`
4. Definir respuestas en `domain.yml`

## 🔒 Seguridad

- **Sanitización**: Todas las entradas del usuario son sanitizadas
- **Validación**: Validación robusta de datos antes de procesar
- **Logging**: Registro de todas las operaciones para auditoría
- **Variables de entorno**: Configuración sensible en archivo .env

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, contactar al equipo de desarrollo.

## 📄 Licencia

Este proyecto es propiedad de [Organización] y está bajo licencia privada. # confirmaciones-bot
