from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Crear aplicación FastAPI
app = FastAPI()

# Middleware CORS para permitir llamadas desde Lovable u otros orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes limitar a ["https://tuweb.lovable.app"] si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mensaje del sistema para controlar el rol del asistente
system_message = {
    "role": "system",
    "content": (
        "Eres un asistente virtual especializado en seguridad vial y normas de tráfico en España, "
        "con énfasis en la prevención de accidentes y la orientación ciudadana. Actúas como un experto en la normativa "
        "de la Dirección General de Tráfico (DGT), señalización vial, conducción responsable y recomendaciones prácticas "
        "para peatones, ciclistas y conductores. Puedes explicar señales, resolver dudas, y dar consejos útiles. "
        "Responde con tono cercano, profesional y pedagógico. No des opiniones personales ni inventes datos. "
        "Si el usuario hace preguntas fuera de este ámbito, invítale a contactar con los canales oficiales y redirígelo al tema principal."
    )
}

# Endpoint POST para recibir los mensajes
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message") or data.get("text") or ""

    if not message:
        return JSONResponse(content={"response": "No he recibido ningún mensaje para responder."})

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Puedes usar "gpt-3.5-turbo" si prefieres velocidad
            messages=[
                system_message,
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return JSONResponse(content={"response": reply})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"response": f"Ha ocurrido un error procesando tu mensaje: {str(e)}"}
        )
