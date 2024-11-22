from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Load the T5 model and tokenizer
model_path = 'D:\\github\\SE4CSAI Project\\ai_server\\AI\\enhance'  # Adjust to your model path
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)
tokenizer = T5Tokenizer.from_pretrained(model_path)

def enhance_description(input_text, max_length=400, min_length=50, 
                        top_k=100, top_p=0.8, do_sample=False, repetition_penalty=2.0, 
                        num_beams=3, early_stopping=True):
    """
    Enhance a description using the T5 model.

    Args:
        input_text (str): The text to enhance.
        max_length (int): Maximum length of the output text.
        min_length (int): Minimum length of the output text.
        top_k (int): The number of highest probability vocabulary tokens to keep for top-k filtering.
        top_p (float): The cumulative probability for top-p filtering.
        do_sample (bool): Whether to sample output tokens.
        repetition_penalty (float): Penalty for repetition in output.
        num_beams (int): Number of beams for beam search.
        early_stopping (bool): Whether to stop beam search early.

    Returns:
        str: The enhanced description.
    """
    try:
        # Tokenize the input text
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(device)

        # Generate enhanced text
        outputs = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            top_k=top_k,
            top_p=top_p,
            do_sample=do_sample,
            repetition_penalty=repetition_penalty,
            num_beams=num_beams,
            early_stopping=early_stopping
        )

        # Decode and return the enhanced text
        enhanced_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return enhanced_text
    except Exception as e:
        return f"Error enhancing description: {e}"
