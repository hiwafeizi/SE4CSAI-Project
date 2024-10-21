import pandas as pd

# Load the dataset
data = pd.read_csv('sample/form2description.csv')

# Prepare Form2Description input (all columns except 'text') and output (description)
def prepare_form2description_data(data):
    form_input = data.drop(columns=['text'])  # Use all columns except 'text'
    form_input_str = form_input.apply(lambda x: ', '.join(x.astype(str)), axis=1)  # Convert form data to a single string
    form2description = pd.DataFrame({'input': form_input_str, 'output': data['text']})  # Create DataFrame with input/output
    return form2description

# Prepare Description2Form input (description) and output (all columns except 'text')
def prepare_description2form_data(data):
    description_input = data['text']  # Description is the input
    description_output_str = data.drop(columns=['text']).apply(lambda x: ', '.join(x.astype(str)), axis=1)  # Combine all other columns into a string
    description2form = pd.DataFrame({'input': description_input, 'output': description_output_str})
    return description2form

# Get the processed datasets for both models
form2description_data = prepare_form2description_data(data)
description2form_data = prepare_description2form_data(data)

print(description2form_data.head())
print(form2description_data.head())