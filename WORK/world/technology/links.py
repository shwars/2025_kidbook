import re
import json
from pymorphy3 import MorphAnalyzer
from pathlib import Path
from itertools import product

def process_markdown_files(md_folder, concepts_file):
    with open(concepts_file, 'r', encoding='utf-8') as f:
        concepts_data = json.load(f)
    
    term_to_definition_file = {
        term: definition_file 
        for term, definition_file in concepts_data.get('concepts', {}).items()
    }
    
    file_to_terms = {}
    for term, filepath in term_to_definition_file.items():
        file_to_terms.setdefault(filepath, set()).add(term)
    
    morph = MorphAnalyzer()
    
    for md_file in Path(md_folder).glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        defining_terms = file_to_terms.get(md_file.name, set())
        
        replacements = {}
        
        for term, definition_file in term_to_definition_file.items():
            if term in defining_terms:
                continue

            if ' ' in term:
                words = term.split()
                all_forms = []
                for word in words:
                    parsed = morph.parse(word)[0]
                    word_forms = {f.word for f in parsed.lexeme} | {word}
                    all_forms.append(word_forms)
                
                forms = set()
                for form_combo in product(*all_forms):
                    forms.add('#'.join(form_combo))
            else:
                parsed = morph.parse(term)[0]
                forms = {f.word for f in parsed.lexeme} | {term}
            
            link = f"{definition_file}#{term.lower().replace(' ', '-')}"
            
            for form in forms:
                replacements[form.lower()] = (form, link)
    
        for form_lower in replacements:
            form, link = replacements[form_lower]

            search_phrase = form.replace('#', ' ') if '#' in form else form

            pattern = re.compile(
                rf'(?<![\[#])\b({search_phrase})\b(?!\s*[\]\)])',
                re.IGNORECASE
            )

            content = pattern.sub(
                lambda m: f"[{m.group(1)}]({link})",
                content
            )
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)

process_markdown_files(
    md_folder='KIDBOOK/world/technology',
    concepts_file='WORK/world/technology/concepts.json'
)