import pandas as pd
import langdetect

# Load the dataset
def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Original dataset loaded with {len(data)} rows.")
    return data

# Select only relevant columns for training the model
def select_relevant_columns(data):
    relevant_columns = [
        'Type', 'Breed1', 'Gender', 'Color1',
        'MaturitySize', 'FurLength', 'Vaccinated', 'Dewormed', 'Sterilized', 
        'Health', 'Quantity', 'Fee', 'Description'
    ]
    data = data[relevant_columns]
    print(f"Selected {len(relevant_columns)} relevant columns for training.")
    return data

# Load breed and color mappings from CSV files
def load_mappings(breed_file, color_file):
    breeds = pd.read_csv(breed_file)
    colors = pd.read_csv(color_file)
    
    # Create dictionaries for mapping BreedID and ColorID to their names
    breed_mapping = {row['BreedID']: row['BreedName'] for _, row in breeds.iterrows()}
    color_mapping = {row['ColorID']: row['ColorName'] for _, row in colors.iterrows()}
    
    # Add a default value for `0` to map to 'None'
    breed_mapping[0] = 'None'
    color_mapping[0] = 'None'
    
    print("Breed and color mappings loaded successfully.")
    return breed_mapping, color_mapping

# Define mappings for categorical values
type_mapping = {1: "Dog", 2: "Cat", 0: "None"}  # Assuming 0 means unspecified
gender_mapping = {1: "Male", 2: "Female", 3: "Mixed", 0: "None"}  # Assuming 0 means unspecified
maturity_size_mapping = {1: "Small", 2: "Medium", 3: "Large", 4: "Extra Large", 0: "None"}
fur_length_mapping = {1: "Short", 2: "Medium", 3: "Long", 0: "None"}
vaccinated_mapping = {1: "Yes", 2: "No", 3: "None"}  # Assuming 3 means "Not Sure"
dewormed_mapping = {1: "Yes", 2: "No", 3: "None"}  # Assuming 3 means "Not Sure"
sterilized_mapping = {1: "Yes", 2: "No", 3: "None"}  # Assuming 3 means "Not Sure"
health_mapping = {1: "Healthy", 2: "Minor Injury", 3: "Serious Injury", 0: "None"}

# Filter for AdoptionSpeed of 0, 1, or 2
def filter_adoption_speed(data):
    data = data[data['AdoptionSpeed'].isin([0, 1, 2])]
    print(f"Filtered dataset to {len(data)} rows with AdoptionSpeed 0, 1, or 2.")
    return data

# Filter to keep only English descriptions
def filter_english_descriptions(data):
    print("Filtering English descriptions...")
    english_descriptions = []
    for description in data['Description']:
        try:
            if langdetect.detect(description) == 'en':
                english_descriptions.append(True)
            else:
                english_descriptions.append(False)
        except:
            # If language detection fails, mark as non-English
            english_descriptions.append(False)
    
    data = data[english_descriptions]
    print(f"Filtered dataset to {len(data)} English descriptions.")
    return data

# Replace IDs and categorical values with readable names
def replace_ids_with_names(data, breed_mapping, color_mapping):
    print("Replacing numerical IDs with names...")
    
    data['Type'] = data['Type'].map(type_mapping)
    data['Breed1'] = data['Breed1'].map(breed_mapping)
    data['Gender'] = data['Gender'].map(gender_mapping)
    data['Color1'] = data['Color1'].map(color_mapping)
    data['MaturitySize'] = data['MaturitySize'].map(maturity_size_mapping)
    data['FurLength'] = data['FurLength'].map(fur_length_mapping)
    data['Vaccinated'] = data['Vaccinated'].map(vaccinated_mapping)
    data['Dewormed'] = data['Dewormed'].map(dewormed_mapping)
    data['Sterilized'] = data['Sterilized'].map(sterilized_mapping)
    data['Health'] = data['Health'].map(health_mapping)
    
    print("ID and categorical value replacement complete.")
    return data

# Main function to clean the data in one step and save it
def clean_and_save_data(file_path, breed_file, color_file, output_path):
    # Step 1: Load Data
    data = load_data(file_path)
    
    # Step 4: Filter by AdoptionSpeed (0, 1, 2 only)
    data = filter_adoption_speed(data)

    # Step 2: Select relevant columns early on
    data = select_relevant_columns(data)
    
    # Step 3: Load Breed and Color Mappings
    breed_mapping, color_mapping = load_mappings(breed_file, color_file)

    # Step 5: Filter for English descriptions
    data = filter_english_descriptions(data)
    
    # Step 6: Replace IDs with names
    data = replace_ids_with_names(data, breed_mapping, color_mapping)
    
    # Step 7: Save the cleaned data
    data.to_csv(output_path, index=False)
    print(f"Cleaned data saved to '{output_path}'.")

# Run the data cleaning pipeline
input_file = 'data/train.csv'
breed_file = 'data/PetFinder-BreedLabels.csv'
color_file = 'data/PetFinder-ColorLabels.csv'
output_file = 'data/filtered_train_data.csv'

clean_and_save_data(input_file, breed_file, color_file, output_file)
