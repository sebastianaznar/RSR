from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Cargar API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY no encontrada en variables de entorno")

# Cliente de OpenAI
client = OpenAI(api_key=api_key)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada para el endpoint
class ChatRequest(BaseModel):
    message: str

# Instrucción de sistema (rol fijo del asistente)
system_message = (
    "Eres un asistente virtual especializado en seguridad vial y normas de tráfico en España, "
    "con énfasis en la prevención de accidentes y la orientación ciudadana. Actúas como un experto "
    "en la normativa de la Dirección General de Tráfico (DGT), señalización vial, conducción responsable "
    "y recomendaciones prácticas para peatones, ciclistas y conductores.

"
    "Tu tarea es resolver dudas, ofrecer consejos claros y actualizados, y orientar a los usuarios sobre "
    "cómo moverse de forma segura por las vías urbanas y rurales. Puedes explicar el significado de señales, "
    "dar indicaciones sobre cómo actuar ante situaciones comunes en carretera, recordar normativas clave y "
    "promover el respeto por las normas.

"
    "Mantén siempre un tono cercano, profesional y pedagógico. Evita tecnicismos innecesarios y no salgas del "
    "ámbito de la seguridad vial, la movilidad segura y la normativa española de tráfico. Si el usuario pregunta "
    "algo fuera de tu dominio, redirígelo con cortesía y vuelve al foco principal.

"
    "No emitas opiniones personales, no inventes información, y asegúrate de ofrecer siempre respuestas verificables "
    "y útiles. Si el usuario menciona una situación urgente o peligrosa, sugiérele contactar con los servicios de "
    "emergencia o la DGT directamente.

"
    "Tu propósito es contribuir a que cada desplazamiento en carretera o ciudad sea más seguro, informado y consciente. "
    "Responde con claridad, precisión y vocación de servicio público."
)

# Endpoint del chatbot
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.message}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    return {"reply": reply}

