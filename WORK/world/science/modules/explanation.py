from gigachat import GigaChat

from modules.config import settings

giga = GigaChat(
    credentials=settings.gigachat_auth_key,
    verify_ssl_certs=False,
)

def explain_for_kids(text: str) -> str:
    payload = f"""
        Firstconstraint
        Second
        {text}
    """
    response = giga.chat(payload=payload)
    
    return response.choices[0].message.content
