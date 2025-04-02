from gigachat import GigaChat

from modules.config import settings

giga = GigaChat(
    credentials=settings.gigachat_auth_key,
    verify_ssl_certs=False,
)

def explain_for_kids(text: str, max_tokens: int = 1000) -> str:
    payload = f"""
        Объясни для десятилетнего ребенка:
        {text}
    """
    response = giga.chat(payload=payload, max_tokens=max_tokens)
    
    return response.choices[0].message.content
