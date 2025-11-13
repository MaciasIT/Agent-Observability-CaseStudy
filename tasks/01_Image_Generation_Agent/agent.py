import os
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client
from PIL import Image
import io
from google_adk import Agent, tool
import dotenv
dotenv.load_dotenv()

# --- Configuración del cliente de la API ---
# Lee la API key desde una variable de entorno para mayor seguridad.
api_key = os.environ.get('STABILITY_KEY')
stability_api = None

# Inicializa el cliente de la API solo si se encontró la clave.
if api_key:
    try:
        stability_api = client.StabilityInference(
            key=api_key,
            verbose=True,
            engine="stable-diffusion-xl-1024-v1-0",
        )
    except Exception as e:
        print(f"Error al inicializar el cliente de Stability AI: {e}")
else:
    # Advierte al usuario si no se encuentra la clave. La herramienta no funcionará.
    print("ADVERTENCIA: La variable de entorno STABILITY_KEY no fue encontrada. La herramienta de generación de imágenes no funcionará.")

@tool
def generar_una_imagen(prompt: str, nombre_archivo: str = "output.png"):
    """
    Llama a la API de Stability AI para generar una imagen a partir de un prompt y la guarda en un archivo local.
    Esta herramienta solo puede generar una imagen a la vez.

    Args:
        prompt: La descripción en texto para la imagen a generar.
        nombre_archivo: El nombre del archivo local donde se guardará la imagen.

    Returns:
        La ruta al archivo guardado para confirmar el éxito, o un mensaje de error si falla.
    """
    if not stability_api:
        return "Error: El cliente de la API no está inicializado. Por favor, configura la variable de entorno STABILITY_KEY."

    print(f"\n🤖 Generando imagen para el prompt: '{prompt}'...")
    
    # Llamada a la API
    answers = stability_api.generate(
        prompt=prompt,
        seed=42,
        steps=40,
        cfg_scale=8.0,
        width=1024,
        height=1024,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )
    
    # Procesamiento de la respuesta
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                return "ADVERTENCIA: La solicitud fue filtrada por las políticas de seguridad de la API."
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(nombre_archivo)
                print(f"✅ Imagen guardada como '{nombre_archivo}'")
                return f"Imagen guardada exitosamente como '{nombre_archivo}'"
    
    return "Error: No se pudo generar la imagen."

# --- Definición del Agente ---
root_agent = Agent(
    tools=[generar_una_imagen],
    instructions="""
    Eres un asistente experto en generación de imágenes. Tu objetivo es ayudar a los usuarios a crear imágenes usando las herramientas disponibles.

    ## Reglas de Comportamiento:
    - La herramienta `generar_una_imagen` solo puede crear UNA imagen por llamada.
    - Si el usuario pide una sola imagen (ej: "genera un gato"), usa la herramienta `generar_una_imagen` directamente.
    - Si el usuario pide MÁS DE UNA imagen (ej: "genera 3 imágenes de un perro"), DEBES pedir confirmación antes de proceder. Informa al usuario cuántas imágenes vas a generar y pregúntale si desea continuar.
    - Cuando generes múltiples imágenes tras la confirmación, llama a la herramienta de forma secuencial para cada imagen.
    - Informa siempre al usuario del resultado de la generación.
    - Responde siempre en español.
    """
)
