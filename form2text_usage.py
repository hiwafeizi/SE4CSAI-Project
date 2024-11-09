from transformers import T5Tokenizer, T5ForConditionalGeneration

# Function to load the saved model and tokenizer
def load_model(model_name):
    # Load the tokenizer and the trained model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

# Function to generate description from form input using specified settings
def generate_description(tokenizer, model, form_input, max_length=200):
    # Tokenize the form input
    input_tokens = tokenizer(form_input, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    
    # Generate the description using the specified settings
    outputs = model.generate(
        input_tokens['input_ids'],
        max_length=max_length,
        min_length=50,
        top_k=100,
        top_p=0.8,
        repetition_penalty=4.0,
        num_beams=5,
        do_sample=False,
        early_stopping=True
    )
    
    # Decode the output tokens to get the generated description
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return description

# Load the saved model and tokenizer
tokenizer, model = load_model('AI/form2text')

# List of test cases with form input and expected descriptions
test_data = [
    (
        "Type: Dog, Primary Breed: Labrador, Gender: Male, Primary Color: Black, Maturity Size: Large, Fur Length: Short, Vaccinated: Yes, Dewormed: Yes, Sterilized: No, Health: Healthy, Quantity: 1, Fee: 100",
        "Energetic and loyal Labrador looking for a loving home. Black, large-sized with short fur, vaccinated and dewormed. Needs a family to give him the attention he deserves. Fee: $100."
    ),
    (
        "Type: Cat, Primary Breed: Persian, Gender: Female, Primary Color: White, Maturity Size: Medium, Fur Length: Long, Vaccinated: No, Dewormed: Not Sure, Sterilized: Yes, Health: Minor Injury, Quantity: 1, Fee: 50",
        "Beautiful white Persian cat with long fur and a gentle temperament. Spayed and ready for adoption despite a minor injury. Looking for a caring home. Adoption fee: $50."
    ),
    (
        "Type: Dog, Primary Breed: Beagle, Gender: Male, Primary Color: Brown, Maturity Size: Medium, Fur Length: Short, Vaccinated: Yes, Dewormed: Yes, Sterilized: Yes, Health: Healthy, Quantity: 1, Fee: 75",
        "Friendly and healthy Beagle, brown and white, ready for adoption. Medium-sized with short fur, fully vaccinated, dewormed, and neutered. Adoption fee: $75."
    ),
    (
        "Type: Cat, Primary Breed: Siamese, Gender: Female, Primary Color: Grey, Maturity Size: Small, Fur Length: Medium, Vaccinated: No, Dewormed: No, Sterilized: Not Sure, Health: Healthy, Quantity: 2, Fee: 0",
        "Two adorable Siamese cats, grey with medium-length fur. These small, healthy cats are playful and looking for a home. Free to a loving family."
    ),
    (
        "Type: Dog, Primary Breed: Poodle, Gender: Mixed, Primary Color: White, Maturity Size: Medium, Fur Length: Long, Vaccinated: Not Sure, Dewormed: No, Sterilized: Yes, Health: Serious Injury, Quantity: 1, Fee: 30",
        "Special needs Poodle with long white fur, recently spayed. Needs attentive care due to a serious injury. Adoption fee: $30."
    ),
]

# Test function to generate descriptions based on these inputs
def test_descriptions(test_data):
    # Load the saved model and tokenizer
    tokenizer, model = load_model('best_model2')
    
    for form_input, expected_description in test_data:
        # Generate description for each form input
        generated_description = generate_description(tokenizer, model, form_input)
        
        # Print the generated and expected descriptions
        print(f"Form Input: {form_input}")
        print(f"Generated Description: {generated_description}")
        print(f"Expected Description: {expected_description}\n")

def run():
    # Run the tests
    test_descriptions(test_data)
test_descriptions(test_data)

