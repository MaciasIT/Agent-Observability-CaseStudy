# Exploración y Mejora de Agentes de IA con Google ADK

Este repositorio documenta un viaje práctico a través del desarrollo, depuración y mejora de agentes de IA utilizando el **Google Agent Development Kit (ADK)**. Partiendo de un ejercicio del curso de 5 días de Google en Kaggle sobre Observabilidad de Agentes, este proyecto se ha extendido para abordar desafíos del mundo real y demostrar un enfoque iterativo en la construcción de sistemas inteligentes.

## 🌟 Puntos Clave del Proyecto

-   **Adaptación a Entornos Locales:** Configuración de un entorno de desarrollo local para un cuaderno diseñado para la nube.
-   **Depuración de Agentes de IA:** Identificación y resolución de errores lógicos y técnicos en el comportamiento de un agente.
-   **Mejora de Capacidades:** Extensión de la funcionalidad del agente mediante la integración de nuevas herramientas especializadas.
-   **Observabilidad en Acción:** Uso de logs y trazas para comprender el "razonamiento" del agente y diagnosticar problemas.
-   **Desarrollo Guiado por Problemas:** Un ejemplo práctico de cómo los desafíos inesperados impulsan el aprendizaje y la innovación.

## 📂 Estructura del Repositorio

-   `day-4a-agent-observability.ipynb`: El cuaderno original de Kaggle, adaptado y modificado con las soluciones implementadas.
-   `research-agent/`: Contiene la definición del agente (`agent.py`) con todas las mejoras y correcciones.
-   `GUIA_ESTUDIO_Y_DEBUG.md`: Una guía detallada que explica el cuaderno sección por sección, incluyendo todas las incidencias encontradas y sus soluciones.
-   `PLUGIN_ROADMAP.md`: Un plan de trabajo para desarrollar un plugin personalizado que extienda aún más la observabilidad del agente.
-   `requirements.txt`: Lista de dependencias de Python necesarias para ejecutar el proyecto.
-   `.env.example`: Archivo de ejemplo para la configuración de la API Key.

## 🚀 El Viaje: Un Caso de Estudio en Desarrollo de Agentes

Este proyecto no fue solo seguir un tutorial, sino una inmersión profunda en los desafíos prácticos del desarrollo de agentes de IA:

1.  **Adaptación de la Nube a lo Local:** El primer paso fue hacer que el cuaderno, originalmente diseñado para Kaggle, funcionara en un entorno de desarrollo local. Esto implicó reemplazar la gestión de secretos específica de Kaggle por una solución robusta basada en `python-dotenv` para cargar la `GOOGLE_API_KEY` de forma segura.

2.  **Depurando el "Razonamiento" del Agente:** El cuaderno presentaba un bug inicial de tipo de dato. Una vez resuelto, surgió un problema más sutil: el agente contaba incorrectamente los artículos de investigación. La solución no fue solo código, sino refinar la **instrucción (prompt)** del agente para que analizara y estructurara correctamente la información de búsqueda antes de contarla. Esto destacó la importancia de la ingeniería de prompts en la lógica del agente.

3.  **Mejorando el Agente con Herramientas Especializadas:** Para ir más allá de un simple conteo, se decidió potenciar el agente. Reemplazamos la herramienta genérica de búsqueda de Google por una herramienta personalizada que utiliza la biblioteca `scholarly` para acceder a Google Scholar. Esto permitió al agente recuperar metadatos detallados como autores, año, editorial y enlaces directos a los artículos.

4.  **La Realidad de la Integración de Bibliotecas Externas:** La integración de `scholarly` no estuvo exenta de desafíos. Nos enfrentamos a bloqueos de API y errores de configuración de proxies, lo que requirió una depuración iterativa y un análisis cuidadoso de los logs. Esta experiencia subrayó la importancia de la resiliencia y la capacidad de diagnóstico en el desarrollo de software.

## 🛠️ Cómo Ejecutar el Proyecto

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2.  **Crear un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate # En Linux/macOS
    # .venv\Scripts\activate # En Windows
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la API Key:**
    -   Obtén tu `GOOGLE_API_KEY` desde [Google AI Studio](https://aistudio.google.com/app/api-keys).
    -   Crea un archivo `.env` en la raíz del proyecto (al mismo nivel que `requirements.txt`) y añade tu clave:
        ```
        GOOGLE_API_KEY="TU_API_KEY_AQUI"
        ```

5.  **Ejecutar el Cuaderno:**
    -   Inicia Jupyter Lab o Jupyter Notebook:
        ```bash
        jupyter lab
        # o
        jupyter notebook
        ```
    -   Abre `day-4a-agent-observability.ipynb` y ejecuta las celdas secuencialmente.

## 💡 Próximos Pasos

Consulta `PLUGIN_ROADMAP.md` para el siguiente desafío: implementar un plugin personalizado para rastrear las llamadas a herramientas.

---

**Autor:** [Tu Nombre/Perfil de LinkedIn]

---