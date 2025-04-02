import wikipedia

wikipedia.set_lang("ru")

categories = {
    "Формальные науки": [
        ("Формальные науки", "formal_science.md"),
        ("Математика", "math.md"),
        ("Алгебра", "algebra.md"),
        ("Статистика", "statistics.md"),
        ("Логика", "logic.md"),
        ("Информатика", "computer_science.md"),
        ("Информационные технологии", "information_technology.md"),
        ("Искусственный интеллект", "artificial_intelligence.md"),
    ],
    "Естественные науки": [
        ("Естественные науки", "natural_science.md"),
        ("Физика", "physics.md"),
        ("Химия", "chemistry.md"),
        ("Биология", "biology.md"),
    ],
    "Науки о жизни": [
        ("Науки о жизни", "science_of_life.md"),
        ("Медицина", "medicine.md"),
        ("Генетика", "genetics.md"),
        ("Ботаника", "botanics.md"),
        ("Экология", "ecology.md"),
    ],
    "Общественные науки": [
        ("Общественные науки", "social_science.md"),
        ("Психология", "psychology.md"),
        ("Социология", "sociology.md"),
        ("Экономика", "economics.md"),
        ("История", "history.md"),
    ],
    "Науки о Земле и космосе": [
        ("Науки о Земле", "earth_and_space_science.md"),
        ("Астрономия", "astronomy.md"),
        ("Геология", "geology.md"),
        ("География", "geography.md"),
    ]
}