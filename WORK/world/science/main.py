from modules.config import settings
from modules.explanation import explain_for_kids
from modules.create_md import create_md_file, is_md_file_exists, get_files_to_create



def main():
    files_to_create = get_files_to_create()
    
    for filename in files_to_create:
        if not is_md_file_exists(settings.kidbook_path + '/world/science', filename):
            create_md_file(settings.kidbook_path + '/world/science', filename, filename)
            print("Created file:", filename + ".md")
        else:
            print("File already exists:", filename + ".md")
            
                 
            
            
    
    
    
if __name__ == "__main__":
    main()
