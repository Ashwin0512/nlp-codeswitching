import random
from google.cloud import translate_v2 as translate
import spacy
import os
nlp = spacy.load("en_core_web_sm")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="autonomous-mote-406310-e1b49eaca29c.json"

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

    phraseIdx = 0
    i = 0

    while i < num_tokens:

        token = tokens[i]

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
    return independent_clauses, adjuncts


def translate_text(text, target_language="hi"):
    # Create a Translate client
    client = translate.Client()

    # Translate the text to the target language
    result = client.translate(text, target_language=target_language)

    # Return the translated text
    return result["input"], result["translatedText"]


def translate_random_clauses(sentence, target_language="hi"):
    independent_clauses = break_into_independent_clauses(sentence)
    translated_clauses = []

    # Randomly choose the clauses to translate
    clauses_to_translate = random.sample(range(len(independent_clauses)), random.randint(1, len(independent_clauses)))

    for i, clause in enumerate(independent_clauses):
        if i in clauses_to_translate:
            input_text, translated_text = translate_text(clause, target_language)
            translated_clauses.append(translated_text)
        else:
            translated_clauses.append(clause)

    code_switched_sentence = " ".join(translated_clauses)
    return code_switched_sentence


sentence = "I need to take a class or find a new friend who likes to generate results"
# sentence = "In the quiet embrace of a moonlit garden, where the fragrant blooms painted the air with an intoxicating allure, their bodies entwined in a slow, sensuous dance, and as the silvery glow of the stars caressed their entangled forms, a symphony of whispered desires and longing sighs echoed in the velvety night, becoming an indelible melody of love etched into the very fabric of their shared existence.."
independent_clauses, adjuncts = break_into_independent_clauses(sentence)
print(independent_clauses)
print(adjuncts)
# code_switched_sentence = translate_random_clauses(sentence, target_language="hi")
# print("Original: ", sentence)
# print("Code-Switched: ", code_switched_sentence)