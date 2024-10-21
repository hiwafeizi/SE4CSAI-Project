from transformers import T5Tokenizer, T5ForConditionalGeneration

# Function to load the saved model and tokenizer
def load_model(model_name):
    # Load the tokenizer and the trained model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

# Function to generate description from form input
def generate_description(tokenizer, model, form_input, max_length=128):
    # Tokenize the form input
    input_tokens = tokenizer(form_input, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    
    # Generate the description using the model
    outputs = model.generate(input_tokens['input_ids'], max_length=max_length)
    
    # Decode the output tokens to get the generated description
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return description

# Load the saved model and tokenizer
tokenizer, model = load_model('form2description-model')

# Example form input (as a single string)
form_input = "US, Black, Dog, Adult, Female, Medium, 3"

# Generate and print the description for the given form data
description = generate_description(tokenizer, model, form_input)
print(f"Generated Description: {description}")
