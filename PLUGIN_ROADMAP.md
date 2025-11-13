
# Roadmap: Creación de un Plugin de Conteo de Herramientas

Este documento describe los pasos para implementar un plugin personalizado para el ADK que cuente el número de veces que se invoca una herramienta durante la sesión de un agente. Seguiremos un enfoque guiado por pruebas (TDD).

## Fase 1: Configuración y Pruebas Iniciales

### Paso 1.1: Crear el archivo de prueba
- **Objetivo:** Establecer el entorno de pruebas.
- **Acción:** Crear un nuevo archivo `tests/test_tool_count_plugin.py`.

### Paso 1.2: Escribir la primera prueba (fallida)
- **Objetivo:** Definir el comportamiento esperado del plugin. La prueba debe fallar porque el plugin aún no existe.
- **Acción:** En `test_tool_count_plugin.py`, escribir una prueba que:
    1.  Cree un agente simple con una herramienta.
    2.  Cree un `InMemoryRunner` y le registre una instancia de un (aún inexistente) `ToolCountPlugin`.
    3.  Ejecute el agente para que utilice la herramienta.
    4.  Asegure (`assert`) que el contador de herramientas del plugin es igual a `1`.

## Fase 2: Implementación del Plugin

### Paso 2.1: Crear el archivo del plugin
- **Objetivo:** Crear la estructura básica del plugin para que la prueba anterior pueda importarlo.
- **Acción:** Crear un nuevo archivo `plugins/tool_count_plugin.py`.

### Paso 2.2: Implementación mínima del `ToolCountPlugin`
- **Objetivo:** Hacer que la prueba pase de "Error de importación" a "Fallo de aserción".
- **Acción:** En `plugins/tool_count_plugin.py`:
    1.  Crear la clase `ToolCountPlugin` que herede de `BasePlugin`.
    2.  En el `__init__`, inicializar un contador `self.tool_count = 0`.
    3.  Definir el callback `before_tool_callback` vacío por ahora.

### Paso 2.3: Implementar la lógica del contador
- **Objetivo:** Hacer que la prueba pase.
- **Acción:** En el `ToolCountPlugin`:
    1.  Dentro del callback `before_tool_callback`, añadir la lógica para incrementar `self.tool_count`.
    2.  Ejecutar las pruebas y verificar que ahora pasan.

## Fase 3: Refinamiento y Pruebas Adicionales

### Paso 3.1: Probar el no incremento (Llamadas a LLM)
- **Objetivo:** Asegurarse de que el contador solo se incrementa con llamadas a herramientas, no con otras acciones.
- **Acción:** Añadir una nueva prueba en `test_tool_count_plugin.py` que ejecute un agente que solo requiera una llamada al LLM (sin herramientas) y verifique que `tool_count` sigue siendo `0`.

### Paso 3.2: Probar múltiples llamadas a herramientas
- **Objetivo:** Garantizar que el contador funciona correctamente para múltiples invocaciones.
- **Acción:** Añadir una prueba que fuerce al agente a llamar a una herramienta varias veces (o a llamar a múltiples herramientas) y verifique que el `tool_count` final es el correcto.

## Fase 4: Integración y Limpieza

### Paso 4.1: Integrar el plugin en el `runner` principal (Opcional)
- **Objetivo:** Ver el plugin en acción en un escenario real.
- **Acción:** Modificar la celda del notebook que inicializa el `InMemoryRunner` para que también incluya nuestro nuevo `ToolCountPlugin` junto al `LoggingPlugin`.

### Paso 4.2: Limpieza de código
- **Objetivo:** Asegurar que el código es limpio y está bien documentado.
- **Acción:**
    1.  Añadir docstrings claros al `ToolCountPlugin` y a sus métodos.
    2.  Revisar el código de las pruebas para que sea legible y fácil de entender.
    3.  Eliminar cualquier `print` o código de depuración innecesario.
