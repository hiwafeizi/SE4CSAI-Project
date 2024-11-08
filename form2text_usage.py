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
tokenizer, model = load_model('best_model')

# List of test cases with form input and expected descriptions
test_data = [
    (
        "1,307,0,2,1,2,7,1,1,2,2,2,1",
        "Hi, GENDER ALL FEMALE LOCATION PENANG few days ago, my friend found a box of abandoned puppies at the back of his house. Apparently, this wasn't the first time this is happening and in previous case the puppies were ran over by vehicle. So in an attempt to prevent similar ending, me and my friend have been taking care of the puppies for last few days. Sadly, we are unable to continue on for long term and we have been contacting no-kill animal shelters to accommodate the 4 puppies, but we have been turned down due to the overcrowded situation in the shelter. We would really appreciate anyone who wants to adopt these little puppies. Please help us to spread the words Thanks :)"
    ),
    (
        "2,265,0,1,4,7,0,2,2,2,2,2,1",
        "Very Cute and Active Very Soft Medium Fur Easy to manage Toilet Train (Clumping Sand) Adoption Fees:RM 50 COD Mentari Court Sunway Please Call/SMS(affi)at"
    ),
    (
        "1,307,141,1,5,0,0,2,1,2,1,1,1",
        "follows around and a very clean puppy (will not soil his area)"
    ),
    (
        "2,266,0,2,3,5,0,2,1,2,2,2,1",
        "Found the poor thing while I was out for breakfast , she must have lost her mummy and was following everyone and everything that moves. She was nearly run over a few times !!! Should be less than a month as she still require bottle feeding You can whatsapp or contact me at or"
    ),
    (
        "2,266,0,1,1,7,0,2,1,2,1,2,1",
        "Xiao Bao is highly active healthy cat with long tail. Litter box trained. Passionate cat lover only. If you're really really interested, feel free to contact me via wassap or call."
    )
]

# Test function to generate descriptions based on these inputs
def test_descriptions(tokenizer, model, test_data):
    for form_input, expected_description in test_data:
        # Generate description for each form input
        generated_description = generate_description(tokenizer, model, form_input)
        
        # Print the generated and expected descriptions
        print(f"Form Input: {form_input}")
        print(f"Generated Description: {generated_description}")
        print(f"Expected Description: {expected_description}\n")

# Run the tests
test_descriptions(tokenizer, model, test_data)

