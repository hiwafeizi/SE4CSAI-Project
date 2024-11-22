from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

def load_enhancement_model(model_path):
    """Load the T5 model and tokenizer for enhancing descriptions."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = model.to(device)
    return model, tokenizer, device

def enhance_description(input_text, model, tokenizer, device, max_length=400, min_length=50, 
                        top_k=100, top_p=0.8, do_sample=False, repetition_penalty=2.0, 
                        num_beams=3, early_stopping=True):
    """
    Enhance a description using the T5 model.
    
    Args:
        input_text (str): The text to enhance.
        model: The loaded T5 model.
        tokenizer: The loaded T5 tokenizer.
        device: The device to run the model on (CPU/GPU).
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
    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    inputs = {k: v.to(device) for k, v in inputs.items()}

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

    # Decode the output
    enhanced_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return enhanced_text

# Example usage
if __name__ == "__main__":
    model_path = 'D:\\github\\SE4CSAI Project\\ai_server\\AI\\enhance'  # Adjust to your model path
    model, tokenizer, device = load_enhancement_model(model_path)

    # Input text for enhancement
    input_text = "Found this little one alone near my apartment yesterday. Took it in temporarily to ensure its safety and comfort."

    # Enhance the description
    enhanced_text = enhance_description(input_text, model, tokenizer, device)
    print(f"Input: {input_text}")
    print(f"Enhanced: {enhanced_text}")
