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

# List of test cases with expected descriptions
test_data = [
    ("US, Black, Dog, Adult, Female, Medium, 3", "This sweet girl lost her owner when he recently went to Heaven and she now is looking for her forever home. $200 www.all4animalsrescue.org"),
    ("US, Other, Cat, Baby, Male, Medium, 1", "2 gray kittens, 1 male and 1 female 1 gray tabby female 1 medium length black/gray female 1 medium length black w/gray tips female"),
    ("US, Unknown, Dog, Adult, Male, Small, 2", "Spanky is a 2yr.old cutie, he is 6 pounds and looking for a wonderful home.He is neutered, mico chipped ,heartworm tested and current."),
    ("US, White_Cream, Dog, Adult, Female, Large, 3", "Please call my foster mom, Jody @ (352)316-5155 to find out how sweet I am.. she will be posting my story soon.. Thanks, Ginger"),
    ("US, Other, Cat, Adult, Female, Medium, 1", "I'm Cammy, they are currently working on my bio. Please check back! If you are interested not call or email! Better yet come meet me!"),
    ("US, Other, Cat, Adult, Male, Medium, 1", "I'm CJ, they are currently working on my bio. Please check back! If you are interested not call or email! Better yet come meet me!"),
    ("US, Unknown, Dog, Adult, Male, Large, 3", "Sevier County Humane Society 865-453-7000 959 Gnatty Branch Rd. Sevierville Closed Mondays. Open Tuesday, Wednesday, Thursday 12 - 7 Friday, Saturday, Sunday 12 - 5"),
    ("US, White_Cream, Dog, Baby, Male, Medium, 1", "Adoption fee is $67 and includes vaccinations, spay/neuter, heartworm test, and microchip.        Available for adoption, foster, or rescue.        1869 Ames Blvd  Marrero, LA 70072"),
    ("US, Other, Cat, Adult, Female, Medium, 3", "Misty is a sweet four year old russian blue/lavender tabby. Loves to curl up in your lap. Very sweet. Good with dogs and cats."),
    ("US, Black, Dog, Adult, Female, Large, 1", "Cookie - 4 year old Shepherd mix Female - over 60 lbs (ON DIET!!!) Great with cats, kids, people but would prefer a home without other dogs."),
    ("US, Unknown, Dog, Adult, Male, Small, 1", "Very sweet dog who would love a great home! Jimmy Choo, Border Collie Mix has been shared from Shelter Exchange - http://www.shelterexchange.org."),
    ("US, Unknown, Dog, Adult, Female, Medium, 1", "Very sweet and loving and would love a good home! Dopey, Labrador Retriever Mix has been shared from Shelter Exchange - http://www.shelterexchange.org."),
    ("US, Other, Cat, Adult, Female, Large, 3", "Sandy enjoys playing with and spending time with dogs. Most of all, she love to snuggle and she chirps in her sleep! Best purr ever!"),
    ("US, Unknown, Horse, Adult, Female, Large, 3", "To learn more about Sansa, visit https://horseandridermatch.com/2018/06/08/sansa-2015-palomino-quarter-horse-filly-with-the-appalachian-trainer-face-off/"),
    ("US, Other, Cat, Baby, Male, Medium, 2", "I am a fun, playful, 12 week old handsome little man! Please visit me at Petsmart in Farmingdale or contact me at www.awaprescue.com"),
    ("US, Unknown, Cat, Baby, Male, Medium, 3", "Cute little Tobias was found all alone wondering in the campgrounds. Boy was he hungry! He is safe now and looking for his forever home!"),
    ("US, Unknown, Rat, Young, Male, Medium, 3", "Male hooded rat. Hand tame and sweet. Will do well alone or with a cage mate. Most ages and colors of rats available for adoption."),
    ("US, Unknown, Rat, Young, Male, Medium, 3", "Male hooded rat. Hand tame and sweet. Will do well alone or with a cage mate. Most ages and colors of rats available for adoption."),
    ("US, Other, Cat, Adult, Female, Medium, 3", "Cousin It (spayed female) 3 years - tabby w/ white DSH - stray Front declawed Adoption Fee: $60 Adoption fee includes spay/neuter, up-to-date vaccinations and microchipping."),
    ("US, Black, Dog, Adult, Male, Large, 1", "Blue is friendly, outgoing, active and very smart. He is good with children. His family lost their home and can no longer care for him."),
    ("US, Black, Chicken, Adult, Male, Large, 2", "Axel is a black rooster that is not aggressive around humans, and loves watermelon as his favorite treat. He is looking for his forever home."),
    ("US, Other, Cat, Adult, Female, Small, 1", "FIV/FELV negative Meet Fluffy at pet Valu in Mullica Hil NJ Adopter will need to brush/comb frequently and do eye care from tearing"),
    ("US, Black_White, Cat, Young, Female, Medium, 1", "Evette is a beautiful girl that is very friendly, playful and a cuddler. She is very laid back. Spayed, micro-chipped and current on shots."),
    ("US, Brown_Chocolate, Cat, Adult, Female, Small, 2", "Mocha is a pretty sweet princess. Mocha loves to be petted and curl up in your lap. She gets along with other kitties and dogs."),
]

# Function to generate description for a list of inputs and compare with expected output
def test_descriptions(tokenizer, model, test_data):
    for form_input, expected_description in test_data:
        # Generate description for each form input
        generated_description = generate_description(tokenizer, model, form_input)
        
        # Print the generated and expected descriptions
        print(f"Form Input: {form_input}")
        print(f"Generated Description: {generated_description}")
        print(f"Expected Description: {expected_description}")

# Run the tests
test_descriptions(tokenizer, model, test_data)
