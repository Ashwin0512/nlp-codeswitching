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
    tokens = [token for token in doc]
    num_tokens = len(tokens)

    # Initialize a list to store independent clauses
    independent_clauses = []

    # Initialize a variable to keep track of the current clause
    current_clause = []

    i = 0

    while i < num_tokens:

        token = tokens[i]

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

        elif token.dep_ == "det" and i+1 < num_tokens and (tokens[i+1].pos_ == "NOUN" or tokens[i+1].pos_ == "PROPN") and tokens[i+1].dep_ == "nsubj":
            # print("debug", token.text, tokens[i+1].text)
            if current_clause:
                independent_clauses.append(" ".join(current_clause))
            current_clause = [token.text]
            current_clause.append(tokens[i+1].text)
            i += 1


        elif token.dep_ == "prep" or token.pos_ == "PART" and token.dep_ == "aux" \
        or (token.pos_ == "PRON" or token.pos_ == "PROPN" or token.pos_ == "NOUN") and token.dep_ == "nsubj":##add noun here
        #prep = preposition, pron = pronoun
            if current_clause:
                independent_clauses.append(" ".join(current_clause))
            current_clause = [token.text]  # Reset the current clause

        else:
            current_clause.append(token.text)

        i += 1

    # Add the last clause (or the entire sentence if no comma is found)
    if current_clause:
        independent_clauses.append(" ".join(current_clause))

    return independent_clauses


sentences = ["I was going for a movie yesterday and on the way I met Sudha.",
            "I need to take a class or find a new friend who likes to generate result.",
            "She is tired waiting at the airport.",
            "The cute boy is eating ice-cream in the car.",
            "Originating from the Himalayas, the Ganga is a holy river.",
            "There are a few men standing outside the palace.",
            "Needs someone to explain lambda calculus to him.",
            "But they make it main focus."]

for sentence in sentences:
    independent_clauses = break_into_independent_clauses(sentence)
    print(independent_clauses)

['I was going', 'for a movie yesterday', 'and', 'on the way', 'I met Sudha .']
['I need', 'to take a class', 'or', 'find a new friend', 'who likes', 'to generate result .']
['She is tired waiting', 'at the airport .']
['The cute boy is eating ice - cream', 'in the car .']
['Originating', 'from the Himalayas', 'the Ganga is a holy river .']
['There are a few men standing', 'outside the palace .']
['Needs someone', 'to explain lambda calculus', 'to him .']