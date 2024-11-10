import pandas as pd
import torch
from transformers import MarianMTModel, MarianTokenizer

# File paths
input_file = 'data/filtered_train_data.csv'
output_file = 'data/degraded_to_high_quality_descriptions.csv'

# Read the high-quality descriptions
df = pd.read_csv(input_file)

# Ensure the 'Description' column exists
if 'Description' not in df.columns:
    raise ValueError("The input CSV must contain a 'Description' column.")

# Lists to store the results
low_quality_descriptions = []
high_quality_descriptions = []

# Set device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize MarianMT models and tokenizers for English-French and French-English
model_en_fr = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-fr').to(device)
tokenizer_en_fr = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-fr')

model_fr_en = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-fr-en').to(device)
tokenizer_fr_en = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-fr-en')

# Function to perform back-translation
def back_translate(text, src_tokenizer, src_model, tgt_tokenizer, tgt_model):
    try:
        # Translate from English to French
        tokens = src_tokenizer(text, return_tensors="pt", padding=True).to(device)
        translated_tokens = src_model.generate(**tokens)
        translated_text = src_tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        # Translate back from French to English
        tokens = tgt_tokenizer(translated_text, return_tensors="pt", padding=True).to(device)
        back_translated_tokens = tgt_model.generate(**tokens)
        back_translated_text = tgt_tokenizer.decode(back_translated_tokens[0], skip_special_tokens=True)

        return back_translated_text
    except Exception as e:
        print(f"Error in back-translation: {e}")
        return None

# Process each Description
for idx, Description in enumerate(df['Description']):
    if pd.isna(Description):  # Skip any NaN descriptions
        low_quality_descriptions.append(None)
        high_quality_descriptions.append(Description)
        continue

    # Perform back-translation
    degraded_description = back_translate(
        Description, tokenizer_en_fr, model_en_fr, tokenizer_fr_en, model_fr_en
    )
    if degraded_description is not None:
        low_quality_descriptions.append(degraded_description)
        high_quality_descriptions.append(Description)

        if idx % 100 == 0:
            print(f"Processed {idx + 1}/{len(df)} descriptions.")
    else:
        print(f"Failed to process Description at index {idx}.")
        low_quality_descriptions.append(None)
        high_quality_descriptions.append(Description)

# Create a DataFrame with the results
output_df = pd.DataFrame({
    'low_quality_description': low_quality_descriptions,
    'high_quality_description': high_quality_descriptions
})

# Drop any rows where back-translation failed
output_df = output_df.dropna(subset=['low_quality_description'])

# Save the paired descriptions to a CSV file
output_df.to_csv(output_file, index=False)

print(f"Back-translated descriptions saved to '{output_file}'.")
