from transformers import MarianMTModel, MarianTokenizer

def load_translation_model(model_path):
    """Load the MarianMT model and tokenizer from the given path."""
    model = MarianMTModel.from_pretrained(model_path)
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    return model, tokenizer

def translate_english_to_dutch(sentence, model, tokenizer, max_length=200):
    """
    Translate an English sentence to Dutch using the MarianMT model.
    
    Args:
        sentence (str): The English sentence to translate.
        model: The loaded MarianMT model.
        tokenizer: The loaded MarianMT tokenizer.
        max_length (int): The maximum length for the generated translation.
        
    Returns:
        str: The translated Dutch sentence.
    """
    # Tokenize the input sentence
    inputs = tokenizer(sentence, return_tensors="pt")
    # Generate the translation
    outputs = model.generate(inputs['input_ids'], max_length=max_length)
    # Decode the translated tokens
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Example usage
if __name__ == "__main__":
    model_path = 'D:\\github\\SE4CSAI Project\\ai_server\\AI\\translate'  # Adjust to your model path
    model, tokenizer = load_translation_model(model_path)

    # Translate an English sentence to Dutch
    english_sentence = "Friendly and healthy Beagle, brown and white, ready for adoption. Medium-sized with short fur, fully vaccinated, dewormed, and neutered. Adoption fee: $75."
    dutch_translation = translate_english_to_dutch(english_sentence, model, tokenizer)
    print(f"English: {english_sentence}")
    print(f"Dutch: {dutch_translation}")
