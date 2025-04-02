import wikipedia
import re
wikipedia.set_lang("ru")

# Настройки для ограничения контента
MAX_SUMMARY_SENTENCES = 3  # Максимум предложений во введении
MAX_SECTION_LENGTH = 1000   # Максимум символов в разделе
MAX_SECTIONS = 2           # Максимум разделов

def extract_essential_content(text):
    """Извлекает только самое важное из текста"""
    # Удаляем все заголовки и лишние переносы
    text = re.sub(r'==.*?==+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Оставляем только первый абзац после очистки
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    essential = paragraphs[0] if paragraphs else ""
    
    # Обрезаем до разумной длины
    return essential[:1000] + "..." if len(essential) > 1000 else essential

def get_concise_info(term):
    """Получаем минимально необходимую информацию о термине"""
    try:
        # Краткое определение (первые 2 предложения)
        summary = wikipedia.summary(term, sentences=MAX_SUMMARY_SENTENCES)
        
        # Дополняем только если определение слишком короткое
        if len(summary) < 500:
            page = wikipedia.page(term, auto_suggest=False)
            content = extract_essential_content(page.content)
            if content:
                return f"# {term}\n\n{summary}\n\n{content}"
        
        return f"# {term}\n\n{summary}"
    
    except wikipedia.DisambiguationError as e:
        return f"# {term}\n\nТермин имеет несколько значений:\n- " + "\n- ".join(e.options[:3])
    except wikipedia.PageError:
        return f"# {term}\n\nИнформация не найдена"
    except Exception:
        return f"# {term}\n\nНе удалось получить информацию"