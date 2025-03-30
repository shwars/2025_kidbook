SELECT DISTINCT ?concept ?conceptLabel ?relation ?linkedConcept ?linkedConceptLabel
WHERE {
  {
    # Базовые связи книги (Q571)
    # Q571 – Книга; Q47461344 – Письменная работа; Q7725634 – Литературное произведение; Q386724 – Культурный объект
    VALUES (?concept ?relation ?linkedConcept) {
      (wd:Q571 wdt:P31 wd:Q47461344)      # Книга (Q571) является экземпляром письменной работы (Q47461344)
      (wd:Q571 wdt:P279 wd:Q7725634)       # Книга (Q571) является подклассом литературного произведения (Q7725634)
      (wd:Q571 wdt:P361 wd:Q386724)        # Книга (Q571) является частью культурного объекта (Q386724)
    }
  }
  UNION
  {
    # Связь книги с автором и его профессией
    # P50 – автор; P106 – профессия
    wd:Q571 wdt:P50 ?author.              # Книга имеет автора
    ?author wdt:P106 ?profession.         # Автор обладает профессией
    BIND(wdt:P106 AS ?relation)           # Связь: профессия (P106)
    BIND(?author AS ?concept)             # Автор выступает в качестве концепта
    BIND(?profession AS ?linkedConcept)   # Профессия автора – связанное понятие
  }
  UNION
  {
    # Жанры книги и их родительские жанры
    # P136 – жанр; P279 – подкласс
    wd:Q571 wdt:P136 ?genre.              # Книга имеет жанр
    ?genre wdt:P279 ?superGenre.          # Жанр принадлежит родительской категории
    BIND(wdt:P279 AS ?relation)           # Связь: подкласс (P279)
    BIND(?genre AS ?concept)              # Жанр как концепт
    BIND(?superGenre AS ?linkedConcept)   # Родительский жанр как связанное понятие
  }
  UNION
  {
    # Компоненты книги и материалы этих компонентов
    # P527 – часть; P279 – подкласс
    wd:Q571 wdt:P527 ?component.          # Книга состоит из компонентов
    ?component wdt:P279 ?material.        # Компоненты классифицируются по материалу
    BIND(wdt:P279 AS ?relation)           # Связь: подкласс (P279)
    BIND(?component AS ?concept)          # Компонент книги как концепт
    BIND(?material AS ?linkedConcept)     # Материал компонента как связанное понятие
  }
  UNION
  {
    # Использование книги и связанные когнитивные процессы
    # P366 – использование; P279 – подкласс
    wd:Q571 wdt:P366 ?use.                # Книга используется в определённом контексте
    ?use wdt:P279 ?cognitiveProcess.      # Этот контекст относится к когнитивным процессам
    BIND(wdt:P279 AS ?relation)           # Связь: подкласс (P279)
    BIND(?use AS ?concept)                # Контекст использования как концепт
    BIND(?cognitiveProcess AS ?linkedConcept)  # Когнитивный процесс как связанное понятие
  }
  UNION
  {
    # Литература (Q8242) и её жанры
    # P136 – жанр
    wd:Q8242 wdt:P136 ?litGenre.          # Литература включает жанры
    BIND(wdt:P136 AS ?relation)           # Связь: жанр (P136)
    BIND(wd:Q8242 AS ?concept)            # Литература как концепт
    BIND(?litGenre AS ?linkedConcept)     # Жанр литературы как связанное понятие
  }
  UNION
  {
    # Литература (Q8242) и профессии в области литературы
    # P106 – профессия
    wd:Q8242 wdt:P106 ?litProfession.     # Литература ассоциируется с определёнными профессиями (например, литературный критик)
    BIND(wdt:P106 AS ?relation)           # Связь: профессия (P106)
    BIND(wd:Q8242 AS ?concept)            # Литература как концепт
    BIND(?litProfession AS ?linkedConcept)  # Профессия в области литературы как связанное понятие
  }
  UNION
  {
    # Литература (Q8242) и её тематическое наполнение
    # P921 – основной предмет
    wd:Q8242 wdt:P921 ?litTopic.          # Литература охватывает определённые темы
    BIND(wdt:P921 AS ?relation)           # Связь: основной предмет (P921)
    BIND(wd:Q8242 AS ?concept)            # Литература как концепт
    BIND(?litTopic AS ?linkedConcept)     # Тематика литературы как связанное понятие
  }
  
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "ru,en". 
    ?concept rdfs:label ?conceptLabel.
    ?linkedConcept rdfs:label ?linkedConceptLabel.
  }
}
LIMIT 150
