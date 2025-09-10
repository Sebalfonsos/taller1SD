from ollama import chat
from ollama import ChatResponse



def generar_keywords(titulo: str, resumen: str, texto: str = "") -> list[str]:
    """
    Genera keywords usando Gemini a partir de título + resumen (+ texto si se pasa).
    Retorna una lista de strings.
    """


    prompt = f"""
    Genera una lista de SOLO 5 palabras clave (keywords) representativas para este artículo.
    Solo responde con las keywords separadas por comas.

    Título: {titulo}
    Resumen: {resumen}
    Texto completo: {texto[:500]}  # limitamos para no enviar demasiado
    """
    response: ChatResponse = chat(model='gemma3:1b', messages=[
    {
        'role': 'user',
        'content': f"{prompt}",
    },
    ])


    
    keywords = [kw.strip() for kw in response.message.content.split(",") if kw.strip()]
    return keywords


