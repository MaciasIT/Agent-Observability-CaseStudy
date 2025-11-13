from google_adk import AdkApp
from tasks.01_Image_Generation_Agent.agent import root_agent

# Crea la aplicación ADK que servirá la interfaz web, usando el agente que definimos.
adk_app = AdkApp(agent=root_agent)
