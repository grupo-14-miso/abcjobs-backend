# APLICACION DE Companies

En esta carpeta se encuentra el codigo fuente y sus pruebas unitarias para el componente de company.

Este proyecto hace uso de pipenv para gestión de dependencias y pytest para el framework de pruebas.

# Estructura de archivos
````
company
├── Dockerfile  #Archivo Dockerfile
├── Pipfile # Declaración de dependencias
├── Pipfile.lock 
├── README.md # Información del aplicativo
├── docker-compose.yml # Declaración de infraestructura para despliegue del aplicativo
├── main.py # Archivo principal de ejecución
├── pytest.ini # Configuración de pruebas unitarias
├── src
│   ├── __init__.py #  Módulo de python src
│   ├── logging.conf
│   └── view
│       ├── __init__.py # Módulo de python view
│       └── company_user_view.py # Servicio de Salud
└── tests
    ├── __init__.py # Módulo de python test
    ├── conftest.py # Declaración de métodos para testing
    └── view
        ├── __init__.py # Módulo de python view
        ├── test_company_view.py #Pruebas componente company
````
El archivo ci_pipeline.yml contiene el pipeline que ejecuta las pruebas.

## Como ejecutar localmente las pruebas

1. Install pipenv
2. Ejecutar pruebas
```
cd company
pipenv shell
pipenv install --dev
pipenv run pytest --cov=src -v -s --cov-fail-under=80
deactivate
```