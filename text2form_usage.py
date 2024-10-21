from transformers import T5Tokenizer, T5ForConditionalGeneration

# Function to load the saved model and tokenizer
def load_model(model_name):
    # Load the tokenizer and the trained model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

# Function to generate form data from a description
def generate_form_data(tokenizer, model, description, max_length=128):
    # Tokenize the description input
    input_tokens = tokenizer(description, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    
    # Generate the form data using the model
    outputs = model.generate(input_tokens['input_ids'], max_length=max_length)
    
    # Decode the output tokens to get the generated form data
    form_data = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return form_data

# Load the saved model and tokenizer
tokenizer, model = load_model('description2form-model')

# Example description input
description = "This sweet dog is looking for a forever home. She's playful, friendly, and loves kids."

# Generate and print the form data for the given description
form_data = generate_form_data(tokenizer, model, description)
print(f"Generated Form Data: {form_data}")
