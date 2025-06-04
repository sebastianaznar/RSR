# Ruta sin Riesgo – Chatbot IA

Backend de chatbot en FastAPI con OpenAI, listo para desplegar en Render.

## Instalación local

1. Crea un archivo `.env` con tu clave:
   OPENAI_API_KEY=sk-...

2. Instala dependencias:
   pip install -r requirements.txt

3. Ejecuta:
   uvicorn main:app --reload

## Despliegue en Render

- Subir este repo a GitHub
- Crear Web Service
- Usar build y start commands del `render.yaml`
- Añadir la variable `OPENAI_API_KEY`
