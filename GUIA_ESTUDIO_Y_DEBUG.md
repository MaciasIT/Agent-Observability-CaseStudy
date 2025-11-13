
# Guía de Estudio y Depuración: Notebook `day-4a-agent-observability.ipynb`

## Introducción

Este documento sirve como una guía de estudio y un registro de depuración para el cuaderno `day-4a-agent-observability.ipynb`. Su propósito es doble:

1.  **Explicar el contenido y los objetivos** de cada sección del cuaderno original.
2.  **Documentar todas las incidencias, errores y mejoras** que surgieron durante la ejecución en un entorno local, junto con los pasos que seguimos para diagnosticarlos y solucionarlos.

Este registro te permitirá no solo comprender el material del curso, sino también aprender de los problemas del mundo real que surgen al adaptar código y depurar agentes de IA.

---

## Parte 1: Guía del Cuaderno Original

### Sección 1: Configuración (`Setup`)

Esta sección inicial prepara el entorno.

-   **1.1: Instalar dependencias:** Informa que `google-adk` ya está instalado en el entorno de Kaggle.
-   **1.2: Configurar la API Key:** Explica cómo configurar la `GOOGLE_API_KEY`. **Aquí tuvimos nuestra primera incidencia.**
-   **1.3: Configurar el logging:** Prepara un archivo `logger.log` para capturar logs de nivel `DEBUG`.
-   **1.4: Configurar el proxy:** Define una función para acceder a la UI web de ADK desde el entorno de Kaggle. **Esta sección la omitimos para la ejecución local.**

### Sección 2: Depuración Práctica con la UI Web de ADK

Esta es la sección principal del ejercicio, donde se depura un agente intencionadamente roto.

-   **2.1: Crear el Agente:** Se crea un agente `research-agent` y se define su comportamiento en `research-agent/agent.py`. Se introduce un bug a propósito: la función `count_papers` espera un `str` en lugar de una `List[str]`.
-   **2.2: Ejecutar el Agente:** Se inicia el servidor `adk web` con `--log_level DEBUG`.
-   **2.3: Probar el Agente:** Se pide al usuario que pruebe el agente y observe que el recuento de artículos es anómalamente grande.
-   **2.4: ¡Tu Turno de Arreglarlo!:** Se guía al usuario para que, usando la pestaña "Events" de la UI, encuentre el bug (el tipo de dato incorrecto) y lo corrija.
-   **2.5: Depurar con Logs Locales:** Se muestra cómo, alternativamente, se puede encontrar la misma información de depuración examinando el archivo `logger.log`. **Aquí tuvimos otra incidencia.**

### Sección 3: Logging en Producción

Esta sección final introduce conceptos más avanzados para cuando no se dispone de una UI web.

-   **3.1-3.2: Plugins y Callbacks:** Se explica que los **Plugins** son la solución para la observabilidad en producción. Se detalla que están compuestos de **Callbacks**, que son "ganchos" que se ejecutan en puntos clave del ciclo de vida del agente (antes/después de una llamada al LLM, a una herramienta, etc.). Se muestra un `CountInvocationPlugin` de ejemplo.
-   **3.3-3.4: `LoggingPlugin` Integrado:** Se presenta el `LoggingPlugin` que ADK ofrece de serie. Se muestra cómo registrarlo en un `InMemoryRunner` para obtener una traza de logs completa de forma programática, sin necesidad de la UI web.

---

## Parte 2: Registro de Incidencias y Soluciones

Este es el registro de todos los problemas que encontramos y cómo los resolvimos.

### Incidencia 1: Carga de la API Key en Entorno Local

-   **Problema:** El código original usaba `UserSecretsClient` de Kaggle, que no existe en un entorno local, impidiendo cargar la `GOOGLE_API_KEY`.
-   **Diagnóstico:** El código era específico de la plataforma Kaggle.
-   **Solución:**
    1.  Instalamos la biblioteca `python-dotenv`.
    2.  Modificamos la celda 1.2 para usar `load_dotenv` y `os.getenv` para leer la clave desde un archivo local `.env`.

### Incidencia 2: El Agente Devuelve un Recuento de Artículos Incorrecto

-   **Problema:** Tras corregir el bug inicial del tipo de dato, el agente seguía devolviendo un recuento incorrecto (ej. 11 artículos en lugar de 1), porque interpretaba cada párrafo de un único resultado de búsqueda como un artículo separado.
-   **Diagnóstico:** La herramienta `google_search` devolvía un único bloque de texto (`str`). El LLM, al intentar pasarlo a la herramienta `count_papers` (que esperaba una lista), "improvisaba" y dividía el texto por párrafos.
-   **Solución:** Mejoramos la instrucción (`prompt`) del `root_agent`, dándole pasos explícitos para:
    1.  Recibir el bloque de texto de la búsqueda.
    2.  **Analizar** ese texto para identificar artículos distintos.
    3.  **Crear una lista de Python** con los artículos identificados.
    4.  Pasar esa nueva lista a `count_papers`.

### Incidencia 3: Mejora - Obtener Metadatos Detallados (Enlaces, Autores)

-   **Problema:** El usuario solicitó que el agente devolviera metadatos ricos (enlaces, autores, año) en lugar de solo un resumen. La herramienta `google_search` era insuficiente.
-   **Diagnóstico:** Se necesitaba una herramienta más especializada que devolviera datos estructurados.
-   **Solución:**
    1.  Propusimos y acordamos usar la biblioteca `scholarly` para buscar en Google Scholar.
    2.  Instalamos la biblioteca con `pip install scholarly`.
    3.  Reescribimos por completo `research-agent/agent.py` para:
        -   Crear una nueva herramienta `search_scholar_papers` que usa `scholarly`.
        -   Eliminar el `google_search_agent` genérico.
        -   Actualizar las instrucciones del `root_agent` para usar la nueva herramienta y presentar los resultados detallados.

### Incidencia 4: Error Constante con `scholarly` (Bloqueo y `TypeError`)

-   **Problema:** La nueva herramienta fallaba consistentemente, devolviendo un error.
-   **Diagnóstico Inicial:** Supusimos que Google Scholar estaba bloqueando las peticiones automatizadas, un problema común que se soluciona con proxies.
-   **Solución (Iterativa):**
    1.  **Intento 1 (Incorrecto):** Modificamos el código para usar `scholarly.use_proxy(pg)`.
    2.  **Error Resultante:** El log reveló un `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`. Esto demostró que mi implementación era incorrecta.
    3.  **Intento 2 (Correcto):** Corregimos el código eliminando la línea `scholarly.use_proxy(pg)`, ya que la biblioteca está diseñada para detectar y usar el `ProxyGenerator` automáticamente. **Este paso solucionó el `TypeError`**.

### Incidencia 5: Los Enlaces de `scholarly` Devuelven 404

-   **Problema:** Aunque la herramienta ya funcionaba, los enlaces (`pub_url`) que devolvía llevaban a páginas de error 404.
-   **Diagnóstico:** El campo `pub_url` no es una URL estable o directa al artículo.
-   **Solución Propuesta (Pausada):**
    1.  Modificar temporalmente la herramienta para que imprimiera en el log la estructura de datos completa del objeto `pub` devuelto por `scholarly`.
    2.  Analizar esa estructura para encontrar un campo de URL más fiable (ej. `eprint_url`).
    3.  Actualizar el código para usar el campo correcto.
    *(Decidimos pausar esta depuración para continuar con el cuaderno).*

### Incidencia 6: El Archivo `logger.log` Aparece Vacío

-   **Problema:** Al ejecutar la celda de la sección 2.5 (`!cat logger.log`), no se mostraba ningún contenido.
-   **Diagnóstico:** El comando `!adk web` inicia un **proceso separado** que no hereda la configuración de `logging` del notebook. Por lo tanto, sus logs se imprimían en la salida de la celda, pero no se escribían en el archivo.
-   **Solución:** Modificamos el comando de ejecución para usar la **redirección de la shell**, un método universal para capturar la salida de un proceso:
    ```bash
    !adk web --log_level DEBUG > logger.log 2>&1
    ```
    Esto redirige tanto la salida estándar (`>`) como la salida de error (`2>&1`) al archivo `logger.log`, solucionando el problema.
