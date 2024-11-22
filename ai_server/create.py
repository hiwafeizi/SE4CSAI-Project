from transformers import T5Tokenizer, T5ForConditionalGeneration

def load_form2text_model(model_path):
    """
    Load the T5 model and tokenizer for generating descriptions from form input.
    """
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    return tokenizer, model

def generate_pet_description(form_input, model, tokenizer, max_length=200, min_length=50, 
                             repetition_penalty=4.0, num_beams=5, do_sample=False, early_stopping=True):
    """
    Generate a pet description from form input using the T5 model.

    Args:
        form_input (str): The form input string with pet details.
        model: The T5 model loaded for generating descriptions.
        tokenizer: The tokenizer corresponding to the model.
        max_length (int): Maximum length of the generated description.
        min_length (int): Minimum length of the generated description.
        repetition_penalty (float): Penalty for repetition in the output.
        num_beams (int): Number of beams for beam search.
        do_sample (bool): Whether to sample tokens.
        early_stopping (bool): Whether to stop beam search early.

    Returns:
        str: The generated pet description.
    """
    # Tokenize the form input
    inputs = tokenizer(form_input, return_tensors="pt", padding=True, truncation=True, max_length=max_length)

    # Generate the output description
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        repetition_penalty=repetition_penalty,
        num_beams=num_beams,
        do_sample=do_sample,
        early_stopping=early_stopping
    )

    # Decode the output tokens to get the description
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return description

# Example usage
if __name__ == "__main__":
    # Load the model and tokenizer
    model_path = 'D:\\github\\SE4CSAI Project\\ai_server\\AI\\form2text'  # Adjust this to your model path
    tokenizer, model = load_form2text_model(model_path)

    # Input form details as a string
    form_input = (
        "Type: Dog, Primary Breed: Labrador, Gender: Male, Primary Color: Black, Maturity Size: Large, "
        "Fur Length: Short, Vaccinated: Yes, Dewormed: Yes, Sterilized: No, Health: Healthy, Quantity: 1, Fee: 100"
    )

    # Generate a description
    generated_description = generate_pet_description(form_input, model, tokenizer)

    print(f"Form Input: {form_input}")
    print(f"Generated Description: {generated_description}")
