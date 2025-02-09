# PVTO

**Programa de Virtualización para Terminales de OpenSim**

## Descripción
PVTO es una herramienta para administrar y controlar instancias de OpenSimulator desde una interfaz basada en terminal. Permite ejecutar, monitorear y enviar comandos a OpenSim de forma remota o local, optimizando la gestión de servidores virtuales.

## Características
- Ejecución de múltiples instancias de OpenSim en hilos separados.
- Interacción en tiempo real con cada instancia a través de WebSockets.
- Integración con Python para manejo directo de la consola.
- Desacoplamiento de la lectura de salida y envío de comandos para mayor eficiencia.
- Optimización en la detección de regiones y procesamiento de respuestas.

## Instalación
1. Clona el repositorio:
   ```sh
   git clone https://github.com/ToquiNovic/PVTO
   cd pvto
   ```
2. Instala las dependencias necesarias:
   ```sh
   pip install -r requirements.txt
   ```
3. Configura las rutas de OpenSimulator en el archivo de configuración.

## Uso
Para iniciar PVTO y gestionar instancias de OpenSim:
```sh
python main.py
```

## Contribución
Si deseas contribuir al proyecto, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la licencia MIT.

