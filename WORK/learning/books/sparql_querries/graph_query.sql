PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX ex: <http://example.org/property/>

SELECT ?subject ?subjectLabel ?relation ?relationLabel ?object ?objectLabel WHERE {
  {
    # 1. Книга как экземпляр: письменная работа
    BIND(wd:Q571 AS ?subject)
    BIND(wdt:P31 AS ?relation)
    BIND(wd:Q47461344 AS ?object)
  }
  UNION
  {
    # 2. Книга как подкласс: литературное произведение
    BIND(wd:Q571 AS ?subject)
    BIND(wdt:P279 AS ?relation)
    BIND(wd:Q7725634 AS ?object)
  }
  UNION
  {
    # 3. Издательство: издательство (Q2085381) через P123
    BIND(wd:Q571 AS ?subject)
    BIND(wdt:P123 AS ?relation)
    BIND(wd:Q2085381 AS ?object)
  }
  UNION
  {
    # 4. Автор: автор (Q482980) через P50
    BIND(wd:Q571 AS ?subject)
    BIND(wdt:P50 AS ?relation)
    BIND(wd:Q482980 AS ?object)
  }
  UNION
  {
    # 5. Форма: форма (Q104624828) через кастомное свойство ex:hasForm
    BIND(wd:Q571 AS ?subject)
    BIND(ex:hasForm AS ?relation)
    BIND(wd:Q104624828 AS ?object)
  }
  UNION
  {
    # 6. Жанр: жанр (Q483394) через P136
    BIND(wd:Q571 AS ?subject)
    BIND(wdt:P136 AS ?relation)
    BIND(wd:Q483394 AS ?object)
  }
  UNION
  {
    # От "форма" (Q104624828) → проза (Q676)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q676 AS ?object)
  }
  UNION
  {
    # От "форма" → поэма (Q5185279)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q5185279 AS ?object)
  }
  UNION
  {
    # От "форма" → роман (Q8261)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q8261 AS ?object)
  }
  UNION
  {
    # От "форма" → повесть (Q149537)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q149537 AS ?object)
  }
  UNION
  {
    # От "форма" → энциклопедия (Q5292)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q5292 AS ?object)
  }
  UNION
  {
    # От "форма" → словарь (Q23622)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q23622 AS ?object)
  }
  UNION
  {
    # От "форма" → антология (Q105420)
    BIND(wd:Q104624828 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q105420 AS ?object)
  }
  UNION
  {
    # От "жанр" (Q483394) → драма (Q25372)
    BIND(wd:Q483394 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q25372 AS ?object)
  }
  UNION
  {
    # От "жанр" → триллер (Q182015)
    BIND(wd:Q483394 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q182015 AS ?object)
  }
  UNION
  {
    # От "жанр" → детектив (Q186424)
    BIND(wd:Q483394 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q186424 AS ?object)
  }
  UNION
  {
    # От "жанр" → фантастика (Q8253972)
    BIND(wd:Q483394 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q8253972 AS ?object)
  }
  UNION
  {
    # От "жанр" → фэнтези (Q132311)
    BIND(wd:Q483394 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q132311 AS ?object)
  }
  UNION
  {
    # От "жанр" → техническое (Q1391420)
    BIND(wd:Q483394 AS ?subject)
    BIND(ex:hasSubtype AS ?relation)
    BIND(wd:Q1391420 AS ?object)
  }
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
LIMIT 200
