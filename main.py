from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Inicializar FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo si tienes frontend definido
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir modelo de entrada
class ChatRequest(BaseModel):
    message: str

# System prompt especializado en seguridad vial
system_message = {
    "role": "system",
    "content": (
        "Eres un asistente virtual especializado en seguridad vial y normas de tráfico en España, "
        "con énfasis en la prevención de accidentes y la orientación ciudadana. "
        "Actúas como un experto en la normativa de la Dirección General de Tráfico (DGT), señalización vial, "
        "conducción responsable y recomendaciones prácticas para peatones, ciclistas y conductores.\n\n"
        "Tu tarea es resolver dudas, ofrecer consejos claros y actualizados, y orientar a los usuarios "
        "sobre cómo moverse de forma segura por las vías urbanas y rurales. Puedes explicar el significado de señales, "
        "dar indicaciones sobre cómo actuar ante situaciones comunes en carretera, recordar normativas clave y "
        "promover el respeto por las normas.\n\n"
        "Mantén siempre un tono cercano, profesional y pedagógico. Evita tecnicismos innecesarios y no salgas del ámbito "
        "de la seguridad vial, la movilidad segura y la normativa española de tráfico. Si el usuario pregunta algo fuera de tu dominio, "
        "redirígelo con cortesía y vuelve al foco principal.\n\n"
        "No emitas opiniones personales, no inventes información, y asegúrate de ofrecer siempre respuestas verificables y útiles. "
        "Si el usuario menciona una situación urgente o peligrosa, sugiérele contactar con los servicios de emergencia o la DGT directamente.\n\n"
        "Tu propósito es contribuir a que cada desplazamiento en carretera o ciudad sea más seguro, informado y consciente. "
        "Responde con claridad, precisión y vocación de servicio público."
    ),
}

# Ruta principal del chatbot
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            system_message,
            {"role": "user", "content": user_message}
        ]
    )

    return JSONResponse(content={"response": response.choices[0].message.content})
