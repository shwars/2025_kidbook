#defaultView:Graph
SELECT DISTINCT ?item1 ?item1Label ?relation ?item2 ?item2Label 
                ?article1 ?article2
WHERE {
  {
    VALUES (?item1 ?relation ?item2) {
      (wd:Q747883 wdt:P279 wd:Q349)
      (wd:Q747883 wdt:P279 wd:Q12107964)
      (wd:Q349 wdt:P279 wd:Q1816033)
      (wd:Q349 wdt:P279 wd:Q4438147)
      (wd:Q349 wdt:P279 wd:Q61065)
      (wd:Q349 wdt:P279 wd:Q599867)
    }
  }
  UNION
  {
    ?item2 wdt:P279 wd:Q747883.
    ?item2 ?relation ?item1.
    ?item1 wdt:P279 wd:Q747883.

    FILTER (?item1 NOT IN (wd:Q7198858, wd:Q10265687, wd:Q56296701))
    FILTER (?item2 NOT IN (wd:Q7198858, wd:Q10265687, wd:Q56296701))
  }
  UNION
  {
    ?item2 wdt:P279 wd:Q349.
    ?item2 ?relation ?item1.
    ?item1 wdt:P279 wd:Q349.

    FILTER (?item1 NOT IN (wd:Q7198858, wd:Q10265687, wd:Q56296701, wd:Q5999051, wd:Q1929372, wd:Q1164462, wd:Q878123, wd:Q204686, wd:Q11313135, wd:Q35555522, wd:Q920057, wd:Q18164820, wd:Q21654660, wd:Q733010, wd:Q4443729, wd:Q108429, wd:Q17080486, wd:Q206989, wd:Q5367, wd:Q644628, wd:Q309162, wd:Q3493962, wd:Q31883501, wd:Q60583336, wd:Q5146583, wd:Q1395783))
    FILTER (?item2 NOT IN (wd:Q7198858, wd:Q10265687, wd:Q56296701, wd:Q5999051, wd:Q1929372, wd:Q1164462, wd:Q878123, wd:Q204686, wd:Q11313135, wd:Q35555522, wd:Q920057, wd:Q18164820, wd:Q21654660, wd:Q733010, wd:Q4443729, wd:Q108429, wd:Q17080486, wd:Q206989, wd:Q5367, wd:Q644628, wd:Q309162, wd:Q3493962, wd:Q31883501, wd:Q60583336, wd:Q5146583, wd:Q1395783))
  }


  OPTIONAL {
    ?article1 schema:about ?item1 ;
             schema:isPartOf <https://en.wikipedia.org/> .
  }
  OPTIONAL {
    ?article2 schema:about ?item2 ;
             schema:isPartOf <https://en.wikipedia.org/> .
  }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 50
