from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the trained model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('form2description-model')
tokenizer = T5Tokenizer.from_pretrained('form2description-model')

sample_form_data = {
    "country": ["US", "US", "US"],
    "color_code": ["Black", "Other", "Unknown"],
    "pet": ["Dog", "Cat", "Dog"],
    "age": ["Adult", "Baby", "Adult"],
    "gender": ["Female", "Male", "Male"],
    "size": ["Medium", "Medium", "Small"],
    "photos": [3, 1, 2]
}


# Tokenize the input form data
input_ids = tokenizer(sample_form_data, return_tensors="pt", padding=True, truncation=True).input_ids

# Generate descriptions
outputs = model.generate(input_ids)

# Decode the generated descriptions back to text
generated_descriptions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

# Print the generated descriptions
for i, description in enumerate(generated_descriptions):
    print(f"Form Data: {sample_form_data[i]}")
    print(f"Generated Description: {description}")
    print("-" * 50)
