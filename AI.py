import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer


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


# Split Form2Description data
train_form2description, test_form2description = train_test_split(form2description_data, test_size=0.2)

# Split Description2Form data
train_description2form, test_description2form = train_test_split(description2form_data, test_size=0.2)

# Load the T5 tokenizer
model_name = 't5-small'
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Function to tokenize inputs and outputs
def tokenize_data(data, input_col, output_col):
    input_encodings = tokenizer(data[input_col].tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")
    target_encodings = tokenizer(data[output_col].tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")
    return input_encodings, target_encodings

# Tokenize training data for Form2Description
train_form2description_inputs, train_form2description_targets = tokenize_data(train_form2description, 'input', 'output')

# Tokenize training data for Description2Form
train_description2form_inputs, train_description2form_targets = tokenize_data(train_description2form, 'input', 'output')

from transformers import T5ForConditionalGeneration, AdamW

# Load the T5 model
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Set up optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)

import torch

# Training loop for Form2Description model
model.train()  # Set the model to training mode

# Number of epochs to train
epochs = 30

for epoch in range(epochs):
    optimizer.zero_grad()  # Reset gradients
    outputs = model(input_ids=train_form2description_inputs['input_ids'], labels=train_form2description_targets['input_ids'])
    loss = outputs.loss  # Get the loss
    loss.backward()  # Backpropagate the error
    optimizer.step()  # Update the model parameters
    print(f'Epoch {epoch + 1}, Loss: {loss.item()}')


# Save the trained model and tokenizer
model.save_pretrained('form2description-model')
tokenizer.save_pretrained('form2description-model')
