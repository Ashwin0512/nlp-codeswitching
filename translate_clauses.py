import random
from google.cloud import translate_v2 as translate
import spacy
nlp = spacy.load("en_core_web_sm")

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

    # Initialize a list to store independent clauses
    independent_clauses = []

    # Initialize a variable to keep track of the current clause
    current_clause = []

    for token in doc:
        if token.dep_ == "punct" and token.text == ",":
            # When a comma is encountered, add the current clause to the list
            if current_clause:
                independent_clauses.append(" ".join(current_clause))
            current_clause = []  # Reset the current clause

        elif token.dep_ == "cc": ##cc means conjunction
        # elif token.text.lower() == "and":
            if current_clause:
                independent_clauses.append(" ".join(current_clause))
            independent_clauses.append(token.text)
            current_clause = []  # Reset the current clause

        elif token.dep_ == "prep" or token.pos_ == "PART" and token.dep_ == "aux" \
        or token.pos_ == "PRON" and token.dep_ == "nsubj":
        #prep = preposition, pron = pronoun
            if current_clause:
                independent_clauses.append(" ".join(current_clause))
            current_clause = [token.text]  # Reset the current clause

        else:
            current_clause.append(token.text)

    # Add the last clause (or the entire sentence if no comma is found)
    if current_clause:
        independent_clauses.append(" ".join(current_clause))

    return independent_clauses

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


sentence = "I was going for a movie today, and on the way, I met Sudha."
code_switched_sentence = translate_random_clauses(sentence, target_language="hi")
print("Original: ", sentence)
print("Code-Switched: ", code_switched_sentence)