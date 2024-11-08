from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from rouge import Rouge

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
     "These adorable, healthy puppies were born at the roadside after their mother was abandoned. They are dewormed, vaccinated, and ready for adoption. Please reach out if interested.", "Their pregnant mother was dumped by her irresponsible owner at the roadside near some shops in Subang Jaya. Gave birth to them at the roadside. They are all healthy and adorable puppies. Already dewormed, vaccinated and ready to go to a home. No tying or caging for long hours as guard dogs. However, it is acceptable to cage or tie for precautionary purposes. Interested to adopt pls call me."),
    
    (
     "Miko is a loyal and alert guard dog. She's active and obedient, waiting for the right owner. Contact for more details if interested.", "Good guard dog, very alert, active, obedience waiting for her good master, plz call or sms for more details if you really get interested, thanks!!"),
    
    (
     "Hunter is a playful, adorable puppy who loves to nibble on shoelaces and run around. Seeking a loving home where he will be well-cared for.", "This handsome yet cute boy is up for adoption. He is the most playful pal we've seen in our puppies. He loves to nibble on shoelaces , Chase you at such a young age. Imagine what a cute brat he will be when he grows. We are looking for a loving home for Hunter , one that will take care of him and give him the love that he needs. Please call urgently if you would like to adopt this cutie."),
    
    (
     "A stray kitten found its way to my home. I’ve been feeding it but am unable to keep it.", "This is a stray kitten that came to my house. Have been feeding it, but cannot keep it."),
    
    (
     "Bulat is up for adoption. Currently located in Perak, but willing to arrange for adoption outside the area. Contact for details.", "Anyone within the area of Ipoh or Taiping who is interested to adopt my cat can contact my father at this number (mazuvil) or can just email me. Currently Bulat is at my hometown in Perak, but anyone outside the area can still travel if they want to adopt. There are a lot of cats in my house right now, so I think I should let one of them go to a better owner who can give better attention to him.")
]


# Function to generate enhanced descriptions
def generate_enhancement(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=128, padding="max_length", truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model.generate(inputs["input_ids"], max_length=128, num_beams=4, early_stopping=True)
    enhanced_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return enhanced_text

# Run the tests and calculate similarity scores using ROUGE
def test_model():
    rouge = Rouge()
    total_rouge_score = {'rouge-1': {'f': 0, 'p': 0, 'r': 0}, 'rouge-2': {'f': 0, 'p': 0, 'r': 0}, 'rouge-l': {'f': 0, 'p': 0, 'r': 0}}

    for i, (input_text, expected_output) in enumerate(test_cases, 1):
        generated_output = generate_enhancement(input_text)
        
        # Calculate ROUGE scores
        scores = rouge.get_scores(generated_output, expected_output, avg=True)
        
        for key in total_rouge_score:
            total_rouge_score[key]['f'] += scores[key]['f']
            total_rouge_score[key]['p'] += scores[key]['p']
            total_rouge_score[key]['r'] += scores[key]['r']

        # Output the results
        print(f"Test Case {i}")
        print(f"Input: {input_text}")
        print(f"Expected Output: {expected_output}")
        print(f"Generated Output: {generated_output}")
        print(f"ROUGE Scores: {scores}")
        print("\n" + "-"*50 + "\n")
    
    # Calculate average ROUGE scores
    for key in total_rouge_score:
        total_rouge_score[key]['f'] /= len(test_cases)
        total_rouge_score[key]['p'] /= len(test_cases)
        total_rouge_score[key]['r'] /= len(test_cases)

    print(f"Average ROUGE Scores across test cases: {total_rouge_score}")

if __name__ == "__main__":
    test_model()
