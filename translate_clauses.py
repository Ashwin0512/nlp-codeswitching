import pandas as pd
import numpy as np
import random
from google.cloud import translate_v2 as translate
import spacy
import os
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="autonomous-mote-406310-e1b49eaca29c.json"

def main():
    input_file_path = "/Users/ashwin/Acads/4-1/NLP_Project/CSify/demo/data/split/dev"
    output_file_path = "/Users/ashwin/Acads/4-1/NLP_Project/CSify/demo/data/FinalAlgo/devCSified"

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = [line.strip() for line in input_file]
         
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in tqdm(lines, desc="Processing", unit="sentence"):
            english_sentence, _ = line.split('\t', 1)
            output_file.write(english_sentence + '\n')
            csified_sentence = translate_sentence(english_sentence)
            output_file.write(csified_sentence + '\n')
            output_file.write('\n\n')

def print_structure(sentence):
  doc = nlp(sentence)

  for token in doc:
    ancestors = [t.text for t in token.ancestors]
    children = [t.text for t in token.children]
    print(token.text, "\t", token.i, "\t",
    token.pos_, "\t", token.dep_, "\t\tAncestors: ",
    ancestors, "\n\t\t\t\t\tChildren: ", children)

def break_into_independent_clauses(sentence):
    doc = nlp(sentence)
    tokens = [token for token in doc]
    num_tokens = len(tokens)

    # Initialize a list to store independent clauses
    independent_clauses = []
    adjuncts = []
    indices = {}

    # Initialize a variable to keep track of the current clause
    current_clause = []
    isAdjunct = False
    nounsAdjctives = []

    phraseIdx = 0
    i = 0

    while i < num_tokens:

        token = tokens[i]

        if token.pos_ == "NOUN" or token.pos_ == "ADJ":
            nounsAdjctives.append(token.text)

        if token.dep_ == "punct" and token.text == ",":
            # When a comma is encountered, add the current clause to the list
            if current_clause:
                if isAdjunct:
                    adjuncts.append([phraseIdx, " ".join(current_clause)])
                else:
                    independent_clauses.append([phraseIdx, " ".join(current_clause)])
                isAdjunct = False  
                phraseIdx += 1   
            current_clause = []  # Reset the current clause

        elif token.dep_ == "cc": ##cc means conjunction
            if current_clause:
                if isAdjunct:
                    adjuncts.append([phraseIdx, " ".join(current_clause)])
                else:
                    independent_clauses.append([phraseIdx, " ".join(current_clause)])
                isAdjunct = False
                phraseIdx += 1
                current_clause = [token.text]

            independent_clauses.append([phraseIdx, " ".join(current_clause)])
            phraseIdx += 1
            current_clause = []  # Reset the current clause

        elif token.dep_ == "det" and i+1 < num_tokens and (tokens[i+1].pos_ == "NOUN" or tokens[i+1].pos_ == "PROPN") and tokens[i+1].dep_ == "nsubj":
            # print("debug", token.text, tokens[i+1].text)
            if current_clause:
                if isAdjunct:
                    adjuncts.append([phraseIdx, " ".join(current_clause)])
                else:
                    independent_clauses.append([phraseIdx, " ".join(current_clause)])
                isAdjunct = False
                phraseIdx += 1
            current_clause = [token.text]
            current_clause.append(tokens[i+1].text)
            i += 1


        elif token.dep_ == "prep" or token.pos_ == "PART" and token.dep_ == "aux" \
        or (token.pos_ == "PRON" or token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "nsubj":##add noun here
        #prep = preposition, pron = pronoun

            #     adjuncts.append(current_clause)

            if current_clause:
                if isAdjunct:
                    adjuncts.append([phraseIdx, " ".join(current_clause)])
                else:
                    independent_clauses.append([phraseIdx, " ".join(current_clause)])
                phraseIdx += 1
                # isAdjunct = False
            current_clause = [token.text]  # Reset the current clause'

            if token.dep_ == "prep" or token.pos_ == "PART" and token.dep_ == "aux":
                isAdjunct = True

        else:
            current_clause.append(token.text)

        i += 1

    # Add the last clause (or the entire sentence if no comma is found)
    if current_clause:
        if isAdjunct:
            adjuncts.append([phraseIdx, " ".join(current_clause)])
        else:
            independent_clauses.append([phraseIdx, " ".join(current_clause)])
        phraseIdx += 1
    return independent_clauses, adjuncts, nounsAdjctives

def translate_text(text, target_language="hi"):
    # Create a Translate client
    client = translate.Client()

    # Translate the text to the target language
    result = client.translate(text, target_language=target_language)

    # Return the translated text
    return result["input"], result["translatedText"]

def translate_sentence(sentence, target_language="hi"):
    independent_clauses, adjuncts, nounsAdjctives = break_into_independent_clauses(sentence)

    # print(independent_clauses)
    # print(adjuncts)

    translated_independent_clauses = []
    translated_adjuncts = []

    # Randomly choose the clauses to translate
    clauses_to_translate = random.sample(range(len(independent_clauses)), random.randint(1, len(independent_clauses)))

    for i, clause in enumerate(independent_clauses):
        if i in clauses_to_translate:
            input_text, translated_text = translate_text(clause[1], target_language)
            translated_independent_clauses.append([clause[0],translated_text])
        else:
            translated_independent_clauses.append(clause)

    for i, clause in enumerate(adjuncts):
        words = clause[1].split()
        for j,word in enumerate(words):
            if word in nounsAdjctives:
                toTranslate = random.choice([0,1])
                if toTranslate:
                    actual, translated = translate_text(word)
                    words[j] = translated
        
        translatedSentence = " ".join(words)
        translated_adjuncts.append([clause[0],translatedSentence])

    # print(translated_independent_clauses)
    # print(translated_adjuncts)

    return mergeSentence(translated_independent_clauses, translated_adjuncts)

def mergeSentence(translated_independent_clauses, translated_adjuncts):
    all_translated = translated_independent_clauses + translated_adjuncts
    all_translated = sorted(all_translated, key=lambda x: x[0])
    result = " ".join(phrase[1] for phrase in all_translated)
    return result

if __name__ == "__main__":
    main()
