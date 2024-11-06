from transformers import MarianMTModel, MarianTokenizer
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AdamW
import time
import csv

# Load the English-only descriptions
def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Data loaded successfully. Number of records: {len(data)}")
    return data["text"].tolist()  

# Generate pseudo-labels (English to Dutch translations) and save them in batches
def generate_and_save_pseudo_labels(data, model, tokenizer, output_file="pseudo_labels.csv", write_batch_size=500):
    translations = []
    print("Generating pseudo-labels...")

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["en_text", "nl_text"])  # Write header

        for i, sentence in enumerate(data, 1):
            try:
                # Translate each sentence
                inputs = tokenizer(sentence, return_tensors="pt")
                outputs = model.generate(inputs['input_ids'])
                translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                translations.append([sentence, translated_text])
                
                # Check to ensure translation is correct
                if not translated_text:
                    print(f"Warning: Empty translation at index {i} for sentence: {sentence}")
            
            except Exception as e:
                print(f"Error during translation at index {i}: {e}")
                continue

            # Write in batches
            if i % write_batch_size == 0:
                writer.writerows(translations)
                file.flush()  # Explicitly flush after each batch
                translations = []  # Clear the batch from memory
                print(f"{i}/{len(data)} translations generated and saved.")

        # Write any remaining translations
        if translations:
            writer.writerows(translations)
            file.flush()
            print(f"{len(data)}/{len(data)} translations generated and saved.")
    
    print("Pseudo-label generation and saving complete.")


# Prepare pseudo-labeled dataset for supervised fine-tuning
class TranslationDataset(Dataset):
    def __init__(self, csv_file, tokenizer, max_length=256):
        self.data = pd.read_csv(csv_file)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        src_text = self.data.iloc[idx, 0]
        tgt_text = self.data.iloc[idx, 1]

        src = self.tokenizer(src_text, max_length=self.max_length, truncation=True, padding="max_length", return_tensors="pt")
        tgt = self.tokenizer(tgt_text, max_length=self.max_length, truncation=True, padding="max_length", return_tensors="pt")

        return src['input_ids'].squeeze(), tgt['input_ids'].squeeze()

# Fine-tuning function
def fine_tune_translation_model(model, dataset, epochs=3, batch_size=256, learning_rate=5e-5, save_path="fine_tuned_model"):
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    
    print("Starting fine-tuning...")
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        epoch_start = time.time()
        for batch_num, (src, tgt) in enumerate(dataloader, 1):
            optimizer.zero_grad()
            outputs = model(input_ids=src, labels=tgt)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
            if batch_num % 50 == 0:
                print(f"Epoch {epoch + 1}, Batch {batch_num}/{len(dataloader)}, Batch Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(dataloader)
        epoch_end = time.time()
        print(f"Epoch {epoch + 1}/{epochs} complete. Avg Loss: {avg_loss:.4f}, Epoch Time: {epoch_end - epoch_start:.2f} seconds")
    
    print("Fine-tuning complete. Saving the model...")
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"Model and tokenizer saved to '{save_path}'")

    return model

# Load and translate English descriptions to create a pseudo-labeled dataset
data = load_data('data/form2description_reduced.csv')
model_name = "Helsinki-NLP/opus-mt-en-nl"  # Example model for English to Dutch
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

# Generate and save pseudo-labels in batches to avoid memory issues
generate_and_save_pseudo_labels(data, model, tokenizer, output_file="pseudo_labels.csv")

# Fine-tune the model on the saved pseudo-labeled dataset
dataset = TranslationDataset("pseudo_labels.csv", tokenizer)
fine_tuned_model = fine_tune_translation_model(model, dataset, save_path="fine_tuned_translation_model")
