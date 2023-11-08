import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.csify import CSify
import google_translate_args
# import deepl_args
import demo

#  This is a demo on how to use the Csify class
if __name__ == '__main__':
    #  Initiate an code-switcher.
    code_switcher = CSify(**google_translate_args.EN_TO_ENHI)
    
    # result = code_switcher.generate("\nyou poured your father's remains in and closed it.\n")
    # result = code_switcher.generate("\nI was going for a movie yesterday and on the way I met Sudha\n")
    # result = code_switcher.generate("\nI need to take a class or find a new friend who likes to generate results\n")
    # print(result)
    # print(bleu)

    """
    This demo function below is defined at ./demo.py
    It downloads and extracts the JESC split corpus, a parallel Japanese-English monolingual corpus.
    Of the extraction results located at ./data/split, we will take the test data (./data/split/test) that contains
    2000 lines and generate code-switched data from it.
    The result will be in 2 files:
    English sentences and code-switched sentences generated from it will be stored in ./data/CSified/EN-Code-Switched
    Japanese sentences and code-switched sentences generated from it will be stored in ./data/CSified/JA-Code-Switched
    This demo also features a progress bar that tracks how many sentences it has generated and its speed in 
    it/s (sentences per second).
    """
    demo.generate_jesc_cs()


    #  you poured तुम्हारे पिता के अवशेष अंदर हैं and closed it . 

# Your last report was दो सप्ताह से अधिक समय पहले  
