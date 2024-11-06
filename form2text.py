import pandas as pd
import time
import torch
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW

# Load the dataset
def load_data(file_path):
    print("Loading dataset...")
    data = pd.read_csv(file_path)
    print(f"Dataset loaded with {data.shape[0]} rows and {data.shape[1]} columns.")
    return data

# Prepare Form2Description input (all columns except 'text') and output (description)
def prepare_form2description_data(data):
    print("Preparing data for Form2Description...")
    form_input = data.drop(columns=['text'])  # Use all columns except 'text'
    form_input_str = form_input.apply(lambda x: ', '.join(x.astype(str)), axis=1)  # Convert form data to a single string
    prepared_data = pd.DataFrame({'input': form_input_str, 'output': data['text']})  # Create DataFrame with input/output
    print("Data preparation complete.")
    return prepared_data

# Custom Dataset class for batching
class TextDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings['input_ids'])

# Tokenize the data and return a DataLoader
def tokenize_data(data, input_col, output_col, tokenizer, batch_size=256):
    print("Tokenizing data...")
    input_encodings = tokenizer(data[input_col].tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")
    target_encodings = tokenizer(data[output_col].tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")
    dataset = TextDataset({"input_ids": input_encodings['input_ids'], "labels": target_encodings['input_ids']})
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    print("Tokenization complete.")
    return dataloader

# Train the model with early stopping and detailed epoch time tracking
def train_model(train_loader, val_loader, tokenizer, model, epochs=30, learning_rate=5e-5, patience=3):
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    model.train()
    
    best_val_loss = float('inf')
    patience_counter = 0
    start_time = time.time()

    for epoch in range(epochs):
        epoch_start_time = time.time()
        
        # Training Phase
        model.train()
        total_train_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            inputs = {key: val.to(model.device) for key, val in batch.items()}
            outputs = model(**inputs)
            train_loss = outputs.loss
            train_loss.backward()
            optimizer.step()
            total_train_loss += train_loss.item()
        
        avg_train_loss = total_train_loss / len(train_loader)
        
        # Validation Phase
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                inputs = {key: val.to(model.device) for key, val in batch.items()}
                outputs = model(**inputs)
                val_loss = outputs.loss
                total_val_loss += val_loss.item()

        avg_val_loss = total_val_loss / len(val_loader)

        epoch_end_time = time.time()
        epoch_duration = epoch_end_time - epoch_start_time
        print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {avg_train_loss:.4f} - Validation Loss: {avg_val_loss:.4f} - Epoch Duration: {epoch_duration:.2f} seconds")

        # Early Stopping Check
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            patience_counter = 0
            save_model(model, tokenizer, "form2text")
            print(f"Model improved at epoch {epoch + 1} and saved as 'best_model'.")
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print("Early stopping triggered.")
            break

    end_time = time.time()
    print(f"Training completed in {(end_time - start_time) / 60:.2f} minutes.")

# Save the model
def save_model(model, tokenizer, model_name):
    print("Saving the model...")
    model.save_pretrained(model_name)
    tokenizer.save_pretrained(model_name)
    print(f"Model and tokenizer saved to '{model_name}'.")

# Main function to orchestrate the process
def run_training_pipeline(file_path, model_name='t5-small', epochs=30, batch_size=256):
    # Load dataset
    data = load_data(file_path)
    
    # Prepare data for Form2Description
    form2description_data = prepare_form2description_data(data)
    
    # Split data
    print("Splitting data into training and validation sets...")
    train_data, val_data = train_test_split(form2description_data, test_size=0.2)
    print(f"Training set size: {len(train_data)} rows, Validation set size: {len(val_data)} rows.")
    
    # Load tokenizer and model
    print("Loading tokenizer and model...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    print("Tokenizer and model loaded.")
    
    # Tokenize data
    train_loader = tokenize_data(train_data, 'input', 'output', tokenizer, batch_size=batch_size)
    val_loader = tokenize_data(val_data, 'input', 'output', tokenizer, batch_size=batch_size)
    
    print("Training starts here...")
    
    # Train the model
    train_model(train_loader, val_loader, tokenizer, model, epochs=epochs)
    
    # Save the final model
    save_model(model, tokenizer, 'form2description-model')

# Run the training pipeline with the dataset
file_path = 'data/form2description_reduced.csv'
run_training_pipeline(file_path, model_name='t5-small', epochs=20, batch_size=256)
