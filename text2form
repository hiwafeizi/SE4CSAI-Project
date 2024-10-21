import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW

# Load the dataset
def load_data(file_path):
    return pd.read_csv(file_path)

# Prepare Description2Form input (text) and output (all columns except 'text')
def prepare_description2form_data(data):
    description_input = data['text']  # 'text' is the input
    form_output_str = data.drop(columns=['text']).apply(lambda x: ', '.join(x.astype(str)), axis=1)  # Combine form data into a string
    return pd.DataFrame({'input': description_input, 'output': form_output_str})  # Create DataFrame with input/output

# Tokenize the data
def tokenize_data(data, input_col, output_col, tokenizer):
    input_encodings = tokenizer(data[input_col].tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")
    target_encodings = tokenizer(data[output_col].tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")
    return input_encodings, target_encodings

# Train the model
def train_model(train_data, tokenizer, model, epochs=30, learning_rate=5e-5):
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    model.train()  # Set the model to training mode
    
    for epoch in range(epochs):
        optimizer.zero_grad()  # Reset gradients
        inputs, targets = train_data
        outputs = model(input_ids=inputs['input_ids'], labels=targets['input_ids'])
        loss = outputs.loss  # Get the loss
        loss.backward()  # Backpropagate the error
        optimizer.step()  # Update the model parameters
        print(f'Epoch {epoch + 1}, Loss: {loss.item()}')

# Save the model
def save_model(model, tokenizer, model_name):
    model.save_pretrained(model_name)
    tokenizer.save_pretrained(model_name)

# Main function to orchestrate the process
def run_training_pipeline(file_path, model_name='t5-small', epochs=30):
    # Load dataset
    data = load_data(file_path)
    
    # Prepare data for Description2Form
    description2form_data = prepare_description2form_data(data)
    
    # Split data
    train_description2form, test_description2form = train_test_split(description2form_data, test_size=0.2)
    
    # Load tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Tokenize data
    train_inputs, train_targets = tokenize_data(train_description2form, 'input', 'output', tokenizer)
    
    print("training starts here")
    
    # Train the model
    train_model((train_inputs, train_targets), tokenizer, model, epochs=epochs)
    
    # Save the trained model
    save_model(model, tokenizer, 'description2form-model')

# Run the training pipeline with the dataset
file_path = 'sample/form2description.csv'
run_training_pipeline(file_path, model_name='t5-small', epochs=30)
