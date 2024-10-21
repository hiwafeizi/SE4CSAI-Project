import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW
import nltk
from nltk.translate.bleu_score import sentence_bleu

# Download necessary NLTK data for BLEU scoring (run once)
# nltk.download('punkt')

# Step 1: Load the Dataset
def load_translation_data(en_file_path, nl_file_path):
    """
    Load the English and Dutch dataset from two separate files.
    """
    with open(en_file_path, 'r', encoding='utf-8') as en_file, open(nl_file_path, 'r', encoding='utf-8') as nl_file:
        en_sentences = en_file.readlines()
        nl_sentences = nl_file.readlines()

    # Create a DataFrame with parallel English-Dutch sentence pairs
    data = pd.DataFrame({'en': [s.strip() for s in en_sentences], 'nl': [s.strip() for s in nl_sentences]})
    return data

# Step 2: Tokenize the Dataset
def tokenize_translation_data(data, tokenizer, max_length=128):
    """
    Tokenize the dataset using the tokenizer from Hugging Face transformers.
    English sentences ('en') are tokenized as input and Dutch sentences ('nl') as target.
    """
    en_inputs = tokenizer(data['en'].tolist(), truncation=True, padding=True, max_length=max_length, return_tensors="pt")
    nl_outputs = tokenizer(data['nl'].tolist(), truncation=True, padding=True, max_length=max_length, return_tensors="pt")
    return en_inputs, nl_outputs

# Step 3: Train the Model
def train_translation_model(model, train_inputs, train_outputs, epochs=3, learning_rate=5e-5):
    """
    Train the translation model using the given inputs and targets.
    """
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    model.train()  # Set model to training mode

    for epoch in range(epochs):
        optimizer.zero_grad()  # Clear gradients

        # Forward pass
        outputs = model(input_ids=train_inputs['input_ids'], labels=train_outputs['input_ids'])
        
        # Compute loss and backward pass
        loss = outputs.loss
        loss.backward()
        optimizer.step()  # Update model parameters

        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}')

    return model

# Step 4: Evaluate the Model
from nltk.tokenize import word_tokenize

def evaluate_translation_model(model, val_data, tokenizer):
    model.eval()  # Set model to evaluation mode
    total_bleu = 0

    for index, row in val_data.iterrows():
        # Prepare input
        inputs = tokenizer(row['en'], return_tensors="pt")
        # Generate translation
        outputs = model.generate(inputs['input_ids'], max_length=50)
        generated_translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        reference_translation = row['nl']

        # Tokenize both the reference and generated translations
        reference_tokens = word_tokenize(reference_translation)
        generated_tokens = word_tokenize(generated_translation)

        # Calculate BLEU score
        bleu_score = sentence_bleu([reference_tokens], generated_tokens)
        total_bleu += bleu_score
        print(f"Input: {row['en']}")
        print(f"Generated: {generated_translation}")
        print(f"Reference: {reference_translation}")
        print(f"BLEU Score: {bleu_score}\n")

    avg_bleu = total_bleu / len(val_data)
    print(f"Average BLEU Score: {avg_bleu}")
    return avg_bleu


# Step 5: Save the Model
def save_translation_model(model, tokenizer, model_name):
    """
    Save the trained model and tokenizer to disk.
    """
    model.save_pretrained(model_name)
    tokenizer.save_pretrained(model_name)
    print(f"Model and tokenizer saved to {model_name}")

# Step 6: Translate a Sentence Using the Model
def translate_sentence(model, tokenizer, sentence):
    """
    Translate a single sentence from English to Dutch.
    """
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=50)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Step 7: Main Function to Run the Training Pipeline
def run_training_pipeline(en_file_path, nl_file_path, model_name='t5-small', epochs=3):
    """
    Run the entire training pipeline: data loading, preprocessing, training, evaluation, and saving.
    """
    # Load dataset
    data = load_translation_data(en_file_path, nl_file_path)
    
    # Split dataset into training and validation sets
    train_data, val_data = train_test_split(data, test_size=0.1)
    
    # Load tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Tokenize training data
    train_inputs, train_outputs = tokenize_translation_data(train_data, tokenizer)
    
    # Train the model
    print("Starting training...")
    trained_model = train_translation_model(model, train_inputs, train_outputs, epochs=epochs)
    
    # Evaluate the model on the validation set
    print("\nEvaluating the model on the validation set...")
    evaluate_translation_model(trained_model, val_data, tokenizer)
    
    # Save the model
    save_translation_model(trained_model, tokenizer, 'translation-model')

# Run the training pipeline with the dataset
en_file_path = 'data/ParaCrawl.en-nl.en'
nl_file_path = 'data/ParaCrawl.en-nl.nl'
run_training_pipeline(en_file_path, nl_file_path, model_name='t5-small', epochs=3)

# Example usage: Translate a single sentence after training
# model = T5ForConditionalGeneration.from_pretrained('translation-model')
# tokenizer = T5Tokenizer.from_pretrained('translation-model')
# sentence = "How are you?"
# print(translate_sentence(model, tokenizer, sentence))
