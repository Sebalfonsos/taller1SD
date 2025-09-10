
from openai import OpenAI


import json

# Cargar la API key desde config.json
with open("config.json", "r") as f:
    config = json.load(f)

client = OpenAI(api_key=config["apikey"], base_url="https://api.deepseek.com")


def generar_keywords(titulo: str, resumen: str, texto: str = "") -> list[str]:
    """
    Genera keywords usando Gemini a partir de título + resumen (+ texto si se pasa).
    Retorna una lista de strings.
    """


    prompt = f"""
    Genera una lista de palabras clave (keywords) representativas para este artículo.
    Solo responde con las keywords separadas por comas.

    Título: {titulo}
    Resumen: {resumen}
    Texto completo: {texto[:1000]}  # limitamos para no enviar demasiado
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"{prompt}"},
        ],
        stream=False    
    )

    # response.text es texto plano tipo "AI, Machine Learning, Deep Learning"
    keywords = [kw.strip() for kw in response.text.split(",") if kw.strip()]
    return keywords


