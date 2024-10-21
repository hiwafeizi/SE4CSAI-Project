import os
import pandas as pd

# Define a function to get a sample without reading the entire file
def get_sample(english_file, dutch_file, sample_size=20):
    english_lines = []
    dutch_lines = []

    # Read only the first 'sample_size' lines from both files
    with open(english_file, 'r', encoding='utf-8') as ef, open(dutch_file, 'r', encoding='utf-8') as df:
        for _ in range(sample_size):
            english_lines.append(ef.readline().strip())
            dutch_lines.append(df.readline().strip())

    # Combine into DataFrame
    parallel_data = pd.DataFrame({
        'English': english_lines,
        'Dutch': dutch_lines
    })

    # Save the sample
    sample_file_path = 'sample/en2dutch.csv'
    os.makedirs('sample', exist_ok=True)
    parallel_data.to_csv(sample_file_path, index=False)

    return parallel_data

# Get a sample from the files (modify paths if necessary)
sample_data = get_sample('data/ParaCrawl.en-nl.en', 'data/ParaCrawl.en-nl.nl')

