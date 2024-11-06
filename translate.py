import os
from transformers import MarianMTModel, MarianTokenizer
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AdamW
import time

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


# Fine-tuning function with checkpoint saving
def fine_tune_translation_model(model, tokenizer, dataset, epochs=1, batch_size=256, learning_rate=5e-5, save_path="fine_tuned_model", save_interval=50):
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
            
            # Print progress every 10 batches
            if batch_num % 10 == 0:
                print(f"Epoch {epoch + 1}, Batch {batch_num}/{len(dataloader)}, Batch Loss: {loss.item():.4f}")
            
            # Save checkpoint at specified intervals
            if batch_num % save_interval == 0:
                checkpoint_path = os.path.join(save_path, f"checkpoint_epoch{epoch+1}_batch{batch_num}")
                os.makedirs(checkpoint_path, exist_ok=True)
                model.save_pretrained(checkpoint_path)
                tokenizer.save_pretrained(checkpoint_path)
                print(f"Checkpoint saved at '{checkpoint_path}'")

        avg_loss = total_loss / len(dataloader)
        epoch_end = time.time()
        print(f"Epoch {epoch + 1}/{epochs} complete. Avg Loss: {avg_loss:.4f}, Epoch Time: {epoch_end - epoch_start:.2f} seconds")
        
        # Save model at the end of each epoch
        epoch_save_path = os.path.join(save_path, f"epoch_{epoch + 1}")
        os.makedirs(epoch_save_path, exist_ok=True)
        model.save_pretrained(epoch_save_path)
        tokenizer.save_pretrained(epoch_save_path)
        print(f"Model and tokenizer saved after epoch {epoch + 1} to '{epoch_save_path}'")

    print("Fine-tuning complete.")
    # Final save
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"Final model and tokenizer saved to '{save_path}'")
    
    return model


# Load the pseudo-labeled dataset
model_name = "Helsinki-NLP/opus-mt-en-nl"  # Example model for English to Dutch
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

# Fine-tune the model on the existing pseudo-labeled dataset
dataset = TranslationDataset("data/pseudo_labels.csv", tokenizer)
fine_tuned_model = fine_tune_translation_model(model, tokenizer, dataset, save_path="fine_tuned_translation_model")
