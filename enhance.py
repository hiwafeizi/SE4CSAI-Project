from transformers import T5ForConditionalGeneration, T5Tokenizer, AdamW, get_linear_schedule_with_warmup
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import time

# Set up device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the dataset
def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Data loaded successfully with {len(data)} records.")
    return data

# Custom Dataset Class
class TextEnhancementDataset(Dataset):
    def __init__(self, dataframe, tokenizer, source_max_token_len=128, target_max_token_len=128):
        self.tokenizer = tokenizer
        self.data = dataframe
        self.source_max_token_len = source_max_token_len
        self.target_max_token_len = target_max_token_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        source_text = self.data.iloc[index]['input']
        target_text = self.data.iloc[index]['target']

        source_encoding = self.tokenizer(
            source_text,
            max_length=self.source_max_token_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        target_encoding = self.tokenizer(
            target_text,
            max_length=self.target_max_token_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        labels = target_encoding['input_ids']
        labels[labels == 0] = -100  # Replace padding token ids of the labels by -100

        return {
            'input_ids': source_encoding['input_ids'].flatten(),
            'attention_mask': source_encoding['attention_mask'].flatten(),
            'labels': labels.flatten()
        }

# Create Data Loaders
def create_data_loader(df, tokenizer, batch_size):
    ds = TextEnhancementDataset(
        dataframe=df,
        tokenizer=tokenizer
    )
    return DataLoader(ds, batch_size=batch_size, num_workers=4)

# Model Training Function with Gradient Accumulation
def train_epoch(model, data_loader, optimizer, scheduler, device, epoch, accumulation_steps=2):
    model.train()
    total_loss = 0
    start_time = time.time()
    print(f"Starting training for epoch {epoch}...")

    for idx, batch in enumerate(data_loader):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        loss = loss / accumulation_steps  # Scale loss for gradient accumulation
        total_loss += loss.item()

        loss.backward()

        if (idx + 1) % accumulation_steps == 0:
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        if idx % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Epoch {epoch}, Batch {idx}/{len(data_loader)}, Loss: {loss.item() * accumulation_steps:.4f}, Time Elapsed: {elapsed:.2f}s")
            start_time = time.time()

    avg_loss = total_loss / len(data_loader)
    print(f"Epoch {epoch} completed. Average Loss: {avg_loss:.4f}")
    return avg_loss

# Model Evaluation Function
def eval_model(model, data_loader, device):
    model.eval()
    total_loss = 0
    print("Starting evaluation...")

    with torch.no_grad():
        for idx, batch in enumerate(data_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            loss = outputs.loss
            total_loss += loss.item()

    avg_loss = total_loss / len(data_loader)
    print(f"Evaluation completed. Average Validation Loss: {avg_loss:.4f}")
    return avg_loss

# Main Function to Train and Save the Model
def train_model(file_path, model_name='t5-base', epochs=30, batch_size=8, learning_rate=3e-5, accumulation_steps=4):
    # Load Data
    df = load_data(file_path)
    print("Data splitting into train and validation sets...")
    
    # Split Data
    train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)
    print(f"Training set size: {len(train_df)}; Validation set size: {len(val_df)}")
    
    # Initialize Tokenizer and Model
    print("Initializing tokenizer and model...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model = model.to(device)
    print("Tokenizer and model initialization complete.")
    
    # Create Data Loaders
    print("Creating data loaders...")
    train_data_loader = create_data_loader(train_df, tokenizer, batch_size)
    val_data_loader = create_data_loader(val_df, tokenizer, batch_size)
    print("Data loaders created successfully.")
    
    # Set Optimizer and Scheduler
    optimizer = AdamW(model.parameters(), lr=learning_rate, correct_bias=True)
    total_steps = len(train_data_loader) * epochs // accumulation_steps
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=int(total_steps * 0.1), num_training_steps=total_steps
    )
    
    best_val_loss = float('inf')  # Track best validation loss for saving
    # Train and Evaluate the Model
    for epoch in range(1, epochs + 1):
        print(f'\n--- Training epoch {epoch}/{epochs} ---')
        train_loss = train_epoch(model, train_data_loader, optimizer, scheduler, device, epoch, accumulation_steps)
        print(f"Training Loss for epoch {epoch}: {train_loss:.4f}")
        
        val_loss = eval_model(model, val_data_loader, device)
        print(f"Validation Loss for epoch {epoch}: {val_loss:.4f}")

        # Save the model only if validation loss improves
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            print("Validation loss improved. Saving model...")
            model.save_pretrained('t5-text-enhancement-model')
            tokenizer.save_pretrained('t5-text-enhancement-model')
    
    print("Training complete. Best model saved to 't5-text-enhancement-model'.")

# Run the training pipeline
if __name__ == "__main__":
    train_model(file_path='data/filtered_train_data.csv')
