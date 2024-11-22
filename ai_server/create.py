from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load the T5 model and tokenizer
model_path = 'D:\\github\\SE4CSAI Project\\ai_server\\AI\\form2text'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)

def generate_pet_description(form_input, max_length=200, min_length=50, 
                             repetition_penalty=4.0, num_beams=5, do_sample=False, early_stopping=True):
    """
    Generate a pet description from form input using the T5 model.

    Args:
        form_input (str): The form input string with pet details.
        max_length (int): Maximum length of the generated description.
        min_length (int): Minimum length of the generated description.
        repetition_penalty (float): Penalty for repetition in the output.
        num_beams (int): Number of beams for beam search.
        do_sample (bool): Whether to sample tokens.
        early_stopping (bool): Whether to stop beam search early.

    Returns:
        str: The generated pet description.
    """
    inputs = tokenizer(form_input, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(device)
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        repetition_penalty=repetition_penalty,
        num_beams=num_beams,
        do_sample=do_sample,
        early_stopping=early_stopping
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
