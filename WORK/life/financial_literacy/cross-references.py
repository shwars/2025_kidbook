import os
import re
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

json_data = {
    "categories": {
        "бюджет": "budget.md",
        "деньги": "budget.md",
        "расходы": "budget.md",
        "тратить": "budget.md",
        "план": "budget.md",
        "карманные": "budget.md",
        "финансы": "budget.md",
        "экономия": "budget.md",
        "кредит": "credit.md",
        "кредитная история": "credit_history.md",
        "денежные дела": "credit_history.md",
        "кредитная история Маши": "credit_history.md",
        "платёж": "credit_history.md",
        "платежи вовремя": "credit_history.md",
        "плохая кредитная история": "credit_history.md",
        "хорошая кредитная история": "credit_history.md",
        "банк": "credit.md",
        "доверие": "credit_history.md",
        "ответственный человек": "credit_history.md",
        "финансовые обязательства": "credit_history.md",
        "срочный платёж": "credit_history.md",
        "покупка": "economy.md",
        "ресурсы": "economy.md",
        "электричество": "economy.md",
        "экономить": "economy.md",
        "оплата услуг": "expenses.md",
        "игрушка-робот": "expenses.md",
        "парк аттракционов": "expenses.md",
        "приоритеты": "expenses.md",
        "накопление": "expenses.md",
        "мечты": "expenses.md",
        "финансовая грамотность": "financial_literacy.md",
        "планирование денег": "financial_literacy.md",
        "долги": "financial_literacy.md",
        "будущее": "financial_literacy.md",
        "финансовый план": "financial_plan.md",
        "цели": "financial_plan.md",
        "откладывать деньги": "financial_plan.md",
        "покупки": "financial_plan.md",
        "футбольный мяч": "financial_plan.md",
        "подарки": "financial_plan.md",
        "велоцикл": "financial_plan.md",
        "поездка в лагерь": "financial_plan.md",
        "блокнот": "financial_plan.md",
        "список продуктов": "financial_plan.md",
        "лишние траты": "financial_plan.md",
        "планировать расходы": "financial_plan.md",
        "необходимое": "financial_plan.md",
        "вкусняшки": "financial_plan.md",
        "составление финансового плана": "financial_plan.md",
        "планирование": "financial_plan.md",
        "финансовые цели": "financial_plan.md",
        "финансовые риски": "financial_risks.md",
        "риски": "financial_risks.md",
        "финансовые потери": "financial_risks.md",
        "кредиты": "financial_risks.md",
        "инфляция": "financial_risks.md",
        "пирожки": "financial_risks.md",
        "ярмарка": "financial_risks.md",
        "прогноз погоды": "financial_risks.md",
        "диверсификация": "financial_risks.md",
        "образование": "financial_risks.md",
        "планирование рисков": "financial_risks.md",
        "финансовое планирование": "financial_risks.md",
        "потеря денег": "financial_risks.md",
        "неудача": "financial_risks.md",
        "доход": "income.md",
        "зарплата": "income.md",
        "конфеты": "income.md",
        "продажа вещей": "income.md",
        "хобби": "income.md",
        "помощь другим": "income.md",
        "доходы": "income.md",
        "управление деньгами": "income.md",
        "отложить деньги": "income.md",
        "работа": "income.md",
        "монетки": "income.md",
        "игрушки": "income.md",
        "рисунки": "income.md",
        "страхование": "insurance.md",
        "страховой взнос": "insurance.md",
        "страховщик": "insurance.md",
        "страхователь": "insurance.md",
        "страховой случай": "insurance.md",
        "велосипед": "insurance.md",
        "страховка": "insurance.md",
        "заболел зуб": "insurance.md",
        "пожар": "insurance.md",
        "авария": "insurance.md",
        "потерялся телефон": "insurance.md",
        "здоровье": "insurance.md",
        "дом": "insurance.md",
        "автомобиль": "insurance.md",
        "ремонт": "insurance.md",
        "инвестиции": "investments.md",
        "акции": "investments.md",
        "прибыль": "investments.md",
        "компания": "investments.md",
        "инвестор": "investments.md",
        "петя": "investments.md",
        "риск": "investments.md",
        "выгода": "investments.md",
        "потерять деньги": "investments.md",
        "перспективы": "investments.md",
        "капитал": "investments.md",
        "доли": "investments.md",
        "американские горки": "investments.md",
        "процент": "percent.md",
        "доля": "percent.md",
        "монеты": "percent.md",
        "выигрыш": "percent.md",
        "карандаши": "percent.md",
        "скидка": "percent.md",
        "товары": "percent.md",
        "цена": "percent.md",
        "рублей": "percent.md",
        "сбережения": "saving.md",
        "копилка": "saving.md",
        "карманные деньги": "saving.md",
        "парк развлечений": "saving.md",
        "непредвиденные расходы": "saving.md",
        "большие покупки": "saving.md",
        "поездка": "saving.md",
        "подарок": "saving.md",
        "цель": "saving.md",
        "копить": "saving.md",
        "копилку": "saving.md",
        "Маша": "saving.md",
        "набор для рисования": "saving.md",
        "картины": "saving.md",
        "цели сбережений": "saving_goals.md",
        "игрушка": "saving_goals.md",
        "поездка к бабушке": "saving_goals.md",
        "пазл": "saving_goals.md",
        "рюкзак": "saving_goals.md",
        "поездка на море": "saving_goals.md",
        "конструктор": "saving_goals.md",
        "сумма": "saving_goals.md",
        "счёт в банке": "saving_goals.md",
        "налог": "tax.md",
        "государство": "tax.md",
        "дорога": "tax.md",
        "школа": "tax.md",
        "больница": "tax.md",
        "работники": "tax.md",
        "полиция": "tax.md",
        "пожарные": "tax.md",
        "налоги": "tax.md",
    }
}

normalized_terms = {
    morph.parse(term)[0].normal_form: (term, path)
    for term, path in json_data["categories"].items()
}

word_pattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
header_pattern = re.compile(r'^\s{0,3}#{1,6}\s')
linked_text_pattern = re.compile(r'\[.*?\]\(.*?\)')


def replace_match(match):
    """ Функция для замены слов на ссылки """
    word = match.group(0)
    lemma = morph.parse(word)[0].normal_form

    if lemma in normalized_terms:
        term, link = normalized_terms[lemma]
        return f"[{word}]({link})"

    return word


def process_markdown_file(file_path):
    """ Обрабатывает Markdown-файл, добавляя ссылки, кроме заголовков. """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if header_pattern.match(line) or linked_text_pattern.search(line):
            updated_lines.append(line)
        else:
            updated_line = word_pattern.sub(replace_match, line)
            updated_lines.append(updated_line)

    updated_content = "".join(updated_lines)
    if updated_content != "".join(lines):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)


directory = "direcrory_path"
md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

for md_file in md_files:
    process_markdown_file(os.path.join(directory, md_file))

print("Обновление ссылок завершено.")
