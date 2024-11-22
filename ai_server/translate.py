from transformers import MarianMTModel, MarianTokenizer

# Load the MarianMT model and tokenizer
model_path = 'D:\\github\\SE4CSAI Project\\ai_server\\AI\\translate'  # Adjust this to your model path
model = MarianMTModel.from_pretrained(model_path)
tokenizer = MarianTokenizer.from_pretrained(model_path)

def translate_english_to_dutch(sentence, max_length=200):
    """
    Translate an English sentence to Dutch using the MarianMT model.

    Args:
        sentence (str): The English sentence to translate.
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
