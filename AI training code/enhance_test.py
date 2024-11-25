from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Define the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the saved model and tokenizer
model_path = 't5-text-enhancement-model'
model = T5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = model.to(device)

# Define test cases with input descriptions and expected enhanced descriptions
test_cases = [

    (
     "Nibble is an energetic, playful kitten, about 3 months old. I’m seeking a responsible new home for him due to limited space and resources.", "Nibble is a 3+ month old ball of cuteness. He is energetic and playful. I rescued a couple of cats a few months ago but could not get them neutered in time as the clinic was fully scheduled. The result was this little kitty. I do not have enough space and funds to care for more cats in my household. Looking for responsible people to take over Nibble's care."),
    
    (
     "Found this little one alone near my apartment yesterday. Took it in temporarily to ensure its safety and comfort.", "I just found it alone yesterday near my apartment. It was shaking so I had to bring it home to provide temporary care."),
    
    (
     "Miko is a loyal and alert guard dog. She's active and obedient, waiting for the right owner. Contact for more details if interested.", "Good guard dog, very alert, active, obedience waiting for her good master, plz call or sms for more details if you really get interested, thanks!!"),
    
    (
     "A stray kitten found its way to my home. I’ve been feeding it but am unable to keep it.", "This is a stray kitten that came to my house. Have been feeding it, but cannot keep it."),
    
    (
     "Bulat is up for adoption. Currently located in Perak, but willing to arrange for adoption outside the area. Contact for details.", "Anyone within the area of Ipoh or Taiping who is interested to adopt my cat can contact my father at this number (mazuvil) or can just email me. Currently Bulat is at my hometown in Perak, but anyone outside the area can still travel if they want to adopt. There are a lot of cats in my house right now, so I think I should let one of them go to a better owner who can give better attention to him.")
]


# Function to generate enhanced descriptions with adjustable parameters
def generate_enhancement(
    input_text, 
    max_length=400, 
    min_length=50, 
    top_k=100, 
    top_p=0.8, 
    do_sample=False, 
    repetition_penalty=4.0, 
    num_beams=5, 
    early_stopping=True
):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate the output with given parameters
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

    enhanced_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return enhanced_text


# Define test cases
test_cases = [
    "Nibble is an energetic, playful kitten, about 3 months old. I’m seeking a responsible new home for him due to limited space and resources.",
    "Found this little one alone near my apartment yesterday. Took it in temporarily to ensure its safety and comfort.",
    "These adorable, healthy puppies were born at the roadside after their mother was abandoned. They are dewormed, vaccinated, and ready for adoption. Please reach out if interested.",
    "These adorable, healthy puppies were born at the roadside after their mother was abandoned. They are dewormed, vaccinated, and ready for adoption. Please reach out if interested.",
    "A stray kitten found its way to my home. I’ve been feeding it but am unable to keep it.",
    
    
]

# Define parameter configurations to test
parameter_configs = [

    {"do_sample": True, "top_k": 200, "top_p": 0.35, "repetition_penalty": 2.0, "num_beams": 3},


]

# Function to run tests with different parameter configurations
def run_tests():
    for config_idx, config in enumerate(parameter_configs, start=1):
        print(f"Testing configuration {config_idx}: {config}")
        for case_idx, input_text in enumerate(test_cases, start=1):
            generated_output = generate_enhancement(
                input_text,
                max_length=400,
                min_length=50,
                **config  # Unpack config dictionary into parameters
            )
            print(f"Test Case {case_idx}")
            print(f"Input: {input_text}")
            print(f"Generated Output: {generated_output}")
            print("\n" + "-"*50 + "\n")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    run_tests()

