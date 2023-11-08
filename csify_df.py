import random
from translate_clauses import translate_random_clauses
from tqdm import tqdm

input_file_path = "demo/data/split/check"
output_file_path = "csified1"

# Function to read the input dataset and extract English sentences
def read_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        english_sentences = [line.split("\t")[0] for line in lines]
        return english_sentences

# Function to write the code-switched dataset
def write_code_switched_dataset(original_sentences, code_switched_sentences, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for original, code_switched in zip(original_sentences, code_switched_sentences):
            file.write(f"{original}\n{code_switched}\n\n")

if __name__ == "__main__":
    # Read the input dataset and extract English sentences
    original_sentences = read_dataset(input_file_path)

    # Initialize the progress bar
    progress_bar = tqdm(total=len(original_sentences), unit="sentence")

    # Generate code-switched sentences
    code_switched_sentences = []
    for sentence in original_sentences:
        code_switched = translate_random_clauses(sentence, target_language="hi")
        code_switched_sentences.append(code_switched)
        progress_bar.update(1)  # Update the progress bar

    # Close the progress bar
    progress_bar.close()

    # Write the code-switched dataset to a new file
    write_code_switched_dataset(original_sentences, code_switched_sentences, output_file_path)