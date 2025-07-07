#!/usr/bin/env python3
"""
Script de validación para verificar que la configuración del bot esté correcta.
"""

import os
import yaml
import logging
from pathlib import Path

# Configurar logging básico
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def validate_yaml_file(file_path: str, description: str) -> bool:
    """
    Valida que un archivo YAML sea válido.
    
    Args:
        file_path: Ruta al archivo YAML
        description: Descripción del archivo para logging
        
    Returns:
        True si el archivo es válido, False en caso contrario
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml.safe_load(file)
        logger.info(f"✅ {description}: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ {description}: {file_path} - Error: {str(e)}")
        return False


def validate_domain_structure(domain_path: str) -> bool:
    """
    Valida la estructura del archivo domain.yml.
    
    Args:
        domain_path: Ruta al archivo domain.yml
        
    Returns:
        True si la estructura es válida, False en caso contrario
    """
    try:
        with open(domain_path, 'r', encoding='utf-8') as file:
            domain = yaml.safe_load(file)
        
        # Verificar elementos requeridos
        required_sections = ['intents', 'entities', 'slots', 'responses', 'actions']
        missing_sections = []
        
        for section in required_sections:
            if section not in domain:
                missing_sections.append(section)
        
        if missing_sections:
            logger.error(f"❌ Domain.yml: Secciones faltantes: {missing_sections}")
            return False
        
        # Verificar intención EXTERNAL_init_context
        if 'EXTERNAL_init_context' not in domain['intents']:
            logger.error("❌ Domain.yml: Intención EXTERNAL_init_context no encontrada")
            return False
        
        # Verificar entidades requeridas
        required_entities = [
            'nombre_paciente', 'id_especialidad', 'especialidad', 'fecha_hora',
            'id_centro_medico', 'centro_medico', 'centro_medico_address',
            'centro_medico_google', 'centro_medico_comuna', 'area_medica',
            'conversation_id', 'bot_name', 'campaign_name', 'phone_number',
            'preparations', 'tipo_mensaje', 'centro_medico_tipo', 'preparation_url',
            'preparation_pdf_name', 'resource_name', 'status', 'piso', 'torre', 'autopago'
        ]
        
        missing_entities = []
        for entity in required_entities:
            if entity not in domain['entities']:
                missing_entities.append(entity)
        
        if missing_entities:
            logger.error(f"❌ Domain.yml: Entidades faltantes: {missing_entities}")
            return False
        
        # Verificar slots correspondientes
        missing_slots = []
        for entity in required_entities:
            if entity not in domain['slots']:
                missing_slots.append(entity)
        
        if missing_slots:
            logger.error(f"❌ Domain.yml: Slots faltantes: {missing_slots}")
            return False
        
        # Verificar slot contexto
        if 'contexto' not in domain['slots']:
            logger.error("❌ Domain.yml: Slot 'contexto' no encontrado")
            return False
        
        # Verificar acción action_init_context
        if 'action_init_context' not in domain['actions']:
            logger.error("❌ Domain.yml: Acción 'action_init_context' no encontrada")
            return False
        
        logger.info("✅ Domain.yml: Estructura válida")
        return True
        
    except Exception as e:
        logger.error(f"❌ Domain.yml: Error validando estructura: {str(e)}")
        return False


def validate_nlu_structure(nlu_path: str) -> bool:
    """
    Valida la estructura del archivo nlu.yml.
    
    Args:
        nlu_path: Ruta al archivo nlu.yml
        
    Returns:
        True si la estructura es válida, False en caso contrario
    """
    try:
        with open(nlu_path, 'r', encoding='utf-8') as file:
            nlu = yaml.safe_load(file)
        
        # Verificar que existe la sección nlu
        if 'nlu' not in nlu:
            logger.error("❌ NLU.yml: Sección 'nlu' no encontrada")
            return False
        
        # Verificar intención EXTERNAL_init_context
        intent_found = False
        for item in nlu['nlu']:
            if 'intent' in item and item['intent'] == 'EXTERNAL_init_context':
                intent_found = True
                break
        
        if not intent_found:
            logger.error("❌ NLU.yml: Intención EXTERNAL_init_context no encontrada")
            return False
        
        logger.info("✅ NLU.yml: Estructura válida")
        return True
        
    except Exception as e:
        logger.error(f"❌ NLU.yml: Error validando estructura: {str(e)}")
        return False


def validate_stories_structure(stories_path: str) -> bool:
    """
    Valida la estructura del archivo stories.yml.
    
    Args:
        stories_path: Ruta al archivo stories.yml
        
    Returns:
        True si la estructura es válida, False en caso contrario
    """
    try:
        with open(stories_path, 'r', encoding='utf-8') as file:
            stories = yaml.safe_load(file)
        
        # Verificar que existe la sección stories
        if 'stories' not in stories:
            logger.error("❌ Stories.yml: Sección 'stories' no encontrada")
            return False
        
        # Verificar historia external init context
        story_found = False
        for story in stories['stories']:
            if 'story' in story and story['story'] == 'external init context':
                story_found = True
                # Verificar que tenga los pasos correctos
                if 'steps' in story:
                    steps = story['steps']
                    if len(steps) >= 2:
                        if steps[0].get('intent') == 'EXTERNAL_init_context' and \
                           steps[1].get('action') == 'action_init_context':
                            logger.info("✅ Stories.yml: Historia external init context válida")
                            return True
        
        if not story_found:
            logger.error("❌ Stories.yml: Historia 'external init context' no encontrada")
            return False
        
        logger.info("✅ Stories.yml: Estructura válida")
        return True
        
    except Exception as e:
        logger.error(f"❌ Stories.yml: Error validando estructura: {str(e)}")
        return False


def validate_rules_structure(rules_path: str) -> bool:
    """
    Valida la estructura del archivo rules.yml.
    
    Args:
        rules_path: Ruta al archivo rules.yml
        
    Returns:
        True si la estructura es válida, False en caso contrario
    """
    try:
        with open(rules_path, 'r', encoding='utf-8') as file:
            rules = yaml.safe_load(file)
        
        # Verificar que existe la sección rules
        if 'rules' not in rules:
            logger.error("❌ Rules.yml: Sección 'rules' no encontrada")
            return False
        
        # Verificar regla para EXTERNAL_init_context
        rule_found = False
        for rule in rules['rules']:
            if 'steps' in rule:
                steps = rule['steps']
                if len(steps) >= 2:
                    if steps[0].get('intent') == 'EXTERNAL_init_context' and \
                       steps[1].get('action') == 'action_init_context':
                        rule_found = True
                        break
        
        if not rule_found:
            logger.error("❌ Rules.yml: Regla para EXTERNAL_init_context no encontrada")
            return False
        
        logger.info("✅ Rules.yml: Estructura válida")
        return True
        
    except Exception as e:
        logger.error(f"❌ Rules.yml: Error validando estructura: {str(e)}")
        return False


def validate_actions_file(actions_path: str) -> bool:
    """
    Valida que el archivo actions.py contenga la clase ActionInitContext.
    
    Args:
        actions_path: Ruta al archivo actions.py
        
    Returns:
        True si la clase está presente, False en caso contrario
    """
    try:
        with open(actions_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if 'class ActionInitContext' in content:
            logger.info("✅ Actions.py: Clase ActionInitContext encontrada")
            return True
        else:
            logger.error("❌ Actions.py: Clase ActionInitContext no encontrada")
            return False
            
    except Exception as e:
        logger.error(f"❌ Actions.py: Error validando archivo: {str(e)}")
        return False


def validate_requirements_file(requirements_path: str) -> bool:
    """
    Valida que el archivo requirements.txt tenga las dependencias correctas.
    
    Args:
        requirements_path: Ruta al archivo requirements.txt
        
    Returns:
        True si las dependencias están correctas, False en caso contrario
    """
    try:
        with open(requirements_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        required_packages = [
            'rasa==3.6.21',
            'rasa-sdk==3.6.2',
            'psycopg2-binary',
            'python-dotenv',
            'requests',
            'jsonschema>=3.2,<4.18',
            'python-dateutil',
            'colorlog'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"❌ Requirements.txt: Paquetes faltantes: {missing_packages}")
            return False
        
        logger.info("✅ Requirements.txt: Dependencias correctas")
        return True
        
    except Exception as e:
        logger.error(f"❌ Requirements.txt: Error validando archivo: {str(e)}")
        return False


def main():
    """
    Función principal de validación.
    """
    logger.info("🔍 Iniciando validación de configuración del bot...")
    
    # Lista de archivos a validar
    files_to_validate = [
        ('config.yml', 'Configuración del pipeline'),
        ('domain.yml', 'Dominio del bot'),
        ('data/nlu.yml', 'Datos de entrenamiento NLU'),
        ('data/stories.yml', 'Historias de conversación'),
        ('data/rules.yml', 'Reglas del bot'),
        ('credentials.yml', 'Credenciales'),
        ('endpoints.yml', 'Endpoints'),
        ('requirements.txt', 'Dependencias del proyecto'),
        ('actions/actions.py', 'Acciones personalizadas'),
        ('actions/database.py', 'Conexión a base de datos'),
        ('actions/utils.py', 'Utilidades'),
        ('logging_config.py', 'Configuración de logging')
    ]
    
    # Validar archivos YAML básicos
    yaml_validation_results = []
    for file_path, description in files_to_validate:
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            result = validate_yaml_file(file_path, description)
            yaml_validation_results.append(result)
    
    # Validaciones específicas
    specific_validations = [
        validate_domain_structure('domain.yml'),
        validate_nlu_structure('data/nlu.yml'),
        validate_stories_structure('data/stories.yml'),
        validate_rules_structure('data/rules.yml'),
        validate_actions_file('actions/actions.py'),
        validate_requirements_file('requirements.txt')
    ]
    
    # Resumen de resultados
    all_results = yaml_validation_results + specific_validations
    passed = sum(all_results)
    total = len(all_results)
    
    logger.info(f"\n📊 Resumen de validación:")
    logger.info(f"✅ Pruebas pasadas: {passed}/{total}")
    logger.info(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        logger.info("🎉 ¡Todas las validaciones pasaron! El bot está configurado correctamente.")
        return True
    else:
        logger.error("⚠️  Algunas validaciones fallaron. Revisa los errores anteriores.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 