SELECT DISTINCT ?item1 ?item1Label ?relation ?item2 ?item2Label 
                ?article1 ?article2
WHERE {
  {
    VALUES (?item1 ?relation ?item2) {
      (wd:Q11629 wdt:P279 wd:Q838948)  # Живопись — подкласс искусства
      (wd:Q860861 wdt:P279 wd:Q838948) # Скульптура — подкласс искусства
      (wd:Q11633 wdt:P279 wd:Q838948)  # Фотография — подкласс искусства
      (wd:Q638 wdt:P279 wd:Q838948)    # Музыка — подкласс искусства
      (wd:Q24354 wdt:P279 wd:Q838948)  # Театр — подкласс искусства
      (wd:Q133311 wdt:P279 wd:Q838948) # Танец — подкласс искусства
      (wd:Q8242 wdt:P279 wd:Q838948)   # Литература — подкласс искусства
      (wd:Q11424 wdt:P279 wd:Q838948)  # Кино — подкласс искусства
      (wd:Q12271 wdt:P279 wd:Q838948)  # Архитектура — подкласс искусства
      (wd:Q36649 wdt:P279 wd:Q838948)  # Графика — подкласс искусства
      (wd:Q17514 wdt:P279 wd:Q838948)  # Декоративно-прикладное искусство — подкласс искусства
      (wd:Q196101 wdt:P279 wd:Q838948) # Цифровое искусство — подкласс искусства
      (wd:Q15544757 wdt:P279 wd:Q838948) # Комиксы — подкласс искусства
      (wd:Q17514 wdt:P279 wd:Q838948)  # Уличное искусство — подкласс искусства
      (wd:Q82604 wdt:P279 wd:Q838948)  # Дизайн — подкласс искусства
    }
  }
  UNION
  {
    ?item2 wdt:P279 wd:Q838948.
    ?item2 ?relation ?item1.
    ?item1 wdt:P279 wd:Q838948.
  }

  OPTIONAL {
    ?article1 schema:about ?item1 ;
             schema:isPartOf <https://en.wikipedia.org/> .
  }
  OPTIONAL {
    ?article2 schema:about ?item2 ;
             schema:isPartOf <https://en.wikipedia.org/> .
  }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru". }
}
LIMIT 100