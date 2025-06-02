from modules.config import settings
from modules.explanation import explain_for_kids
from modules.create_md import create_md_file, is_md_file_exists, get_files_to_create
from modules.links import science_terms
from modules.wiki_content import get_concise_info



def main():
    
    for term in science_terms:
        wiki_info = get_concise_info(term)
        info_for_kids = explain_for_kids(text=wiki_info)
        
        if not is_md_file_exists(settings.kidbook_path + '/world/science', term.lower().replace(' ', '_') + '.md'):
            create_md_file(settings.kidbook_path + '/world/science', term.lower().replace(' ', '_') + '.md', info_for_kids)
            print("Created file:", term.lower().replace(' ', '-') + ".md")
        else:
            print("File already exists:", term.lower().replace(' ', '-') + ".md")
        
        
        
        print(info_for_kids)
        print("=========================================================")  
    
    
    
            
                 
            
            
    
    
    
if __name__ == "__main__":
    main()
