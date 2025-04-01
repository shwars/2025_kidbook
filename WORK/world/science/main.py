from modules.config import settings
from modules.explanation import explain_for_kids


def main():    
    response = explain_for_kids("What is the meaning of life?")
    print(response)
    
if __name__ == "__main__":
    main()
