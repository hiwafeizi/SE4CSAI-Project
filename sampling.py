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
        # Reduce the dataset to only relevant columns (including 'text' for description)
        reduced_data = data[[
            "country", "color_code", "pet", "age", "gender", "size", 
            "photos", 'text'
        ]]
        
        # Save the reduced data (all rows) to a CSV file
        sample_file_path = "data/form2description_reduced.csv"
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(sample_file_path), exist_ok=True)
        
        # Save the reduced data (all rows)
        reduced_data.to_csv(sample_file_path, index=False)
        print(f"\nAll rows with reduced columns saved to {sample_file_path}")
    else:
        print("No data to analyze.")


# Analyze the data for Volume, Variety, and Veracity
def sample_data(data):
    if data is not None:
        # Get the first 200 rows as a sample
        sample_data = data.head(200)
        
        # Save the sample to the CSV file
        sample_file_path = "sample/form2description.csv"
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(sample_file_path), exist_ok=True)
        
        # Save the first 200 rows as a sample
        sample_data.to_csv(sample_file_path, index=False)
        print(f"\nFirst 200 rows saved to {sample_file_path}")
    else:
        print("No data to analyze.")


if __name__ == "__main__":
    # File path to the CSV
    file_path = "data/form2description.csv"
    
    # Load the data
    data = load_data(file_path)
    
    # Perform basic analysis
    analyze_data(data)

        # File path to the CSV
    file_path = "data/form2description_reduced.csv"
    
    # Load the data
    data = load_data(file_path)

    sample_data(data)


