import os
import requests
from dotenv import load_dotenv

# Cargamos las variables del archivo .env si estamos en local
load_dotenv()

class AIService:
    """
    Servicio de IA que consume la Inference API de Hugging Face.
    
    Esta clase utiliza el token de acceso configurado en las variables de entorno
    para autenticar las peticiones a los modelos Open Source de audio y visión.
    """

    def __init__(self):
        """
        Inicializa los headers de autenticación recuperando el token del sistema.
        """
        self.api_token = os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise ValueError("Error: No se encontró la variable HF_API_TOKEN.")
            
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        self.audio_url = "https://api-inference.huggingface.co/models/openai/whisper-tiny"
        self.vision_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"

    def analizar_audio(self, audio_path: str) -> str:
        """
        Envía el archivo de audio a la API de Hugging Face para su transcripción.
        """
        with open(audio_path, "rb") as f:
            data = f.read()
        response = requests.post(self.audio_url, headers=self.headers, data=data)
        return response.json().get("text", "Sin transcripción")