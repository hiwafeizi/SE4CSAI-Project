import os
import pandas as pd

# Load the data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully. Number of records: {len(data)}")
        return data
    except FileNotFoundError:
        print(f"File not found at {file_path}. Please check the path.")
        return None

# Analyze the data for Volume, Variety, and Veracity
def analyze_data(data):
    if data is not None:
        # General information about the dataset
        # print("\nDataset Information:")
        # print(data.info())

        # # Display the first few rows of the data
        # print("\nFirst 5 rows of the dataset:")
        # print(data.head())

        # # Volume: Number of records in the dataset
        # print(f"\nVolume: {len(data)} records")

        # # Variety: Show unique values in columns
        # print("\nVariety: Unique values per column")
        # for column in data.columns:
        #     unique_values = data[column].nunique()
        #     print(f"Column '{column}': {unique_values} unique values")

        # # Veracity: Check for missing or invalid data
        # missing_values = data.isnull().sum()
        # print("\nVeracity: Missing values per column")
        # print(missing_values)

        # # Basic statistics for numerical columns
        # print("\nBasic Statistics:")
        # print(data.describe())

        # # Check for any duplicates in the dataset
        # duplicate_rows = data.duplicated().sum()
        # print(f"\nNumber of duplicate rows: {duplicate_rows}")
        
        # Get and save the first 20 rows as a sample
        sample_data = data.head(2000)
        
        # Save the sample to a CSV file
        sample_file_path = "sample/form2description.csv"
        sample_data.to_csv(sample_file_path, index=False)
        print(f"\nSample data saved to {sample_file_path}")
    else:
        print("No data to analyze.")

if __name__ == "__main__":
    # File path to the CSV
    file_path = "data/form2description.csv"
    
    # Load the data
    data = load_data(file_path)
    
    # Perform basic analysis
    analyze_data(data)


# Define a function to get a sample without reading the entire file
def get_sample(english_file, dutch_file, sample_size=2000):
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
    parallel_data.to_csv(sample_file_path, index=False)

    return parallel_data

# Get a sample from the files (modify paths if necessary)
sample_data = get_sample('data/ParaCrawl.en-nl.en', 'data/ParaCrawl.en-nl.nl')

