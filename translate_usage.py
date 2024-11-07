from transformers import MarianMTModel, MarianTokenizer

# Step 1: Load the saved MarianMT model and tokenizer
model = MarianMTModel.from_pretrained('epoch_1')
tokenizer = MarianTokenizer.from_pretrained('epoch_1')

# Step 2: Define a function for translating sentences
def translate_sentence(model, tokenizer, sentence, max_length=150):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=max_length)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Test cases
test_cases = [
    ("I'm CJ, they are currently working on my bio. Please check back! If you are interested not call or email! Better yet come meet me!",
     "Ik ben CJ, ze werken momenteel aan mijn bio. Kom later nog eens terug! Als je geïnteresseerd bent, bel of e-mail niet! Nog beter, kom me ontmoeten!"),
    
    ("Sevier County Humane Society 865-453-7000 959 Gnatty Branch Rd. Sevierville Closed Mondays. Open Tuesday, Wednesday, Thursday 12 - 7 Friday, Saturday, Sunday 12 - 5",
     "Sevier County Humane Society 865-453-7000 959 Gnatty Branch Rd. Sevierville Gesloten op maandag. Geopend dinsdag, woensdag, donderdag 12 - 7, vrijdag, zaterdag, zondag 12 - 5"),
    
    ("Adoption fee is $67 and includes vaccinations, spay/neuter, heartworm test, and microchip. Available for adoption, foster, or rescue. 1869 Ames Blvd Marrero, LA 70072",
     "Adoptiekosten zijn $67 en omvatten vaccinaties, sterilisatie/castratie, hartwormtest en microchip. Beschikbaar voor adoptie, pleegzorg of redding. 1869 Ames Blvd Marrero, LA 70072"),
    
    ("Misty is a sweet four year old Russian blue/lavender tabby. Loves to curl up in your lap. Very sweet. Good with dogs and cats.",
     "Misty is een lieve vierjarige Russische blauwe/lavendelkleurige tabby. Ze kruipt graag op schoot. Erg lief. Goed met honden en katten."),
    
    ("Cookie - 4 year old Shepherd mix Female - over 60 lbs (ON DIET!!!) Great with cats, kids, people but would prefer a home without other dogs.",
     "Cookie - 4 jaar oude vrouwelijke herdermix - meer dan 60 lbs (OP DIEET!!!) Geweldig met katten, kinderen, mensen, maar zou liever een huis hebben zonder andere honden."),
    
    ("Very sweet dog who would love a great home! Jimmy Choo, Border Collie Mix has been shared from Shelter Exchange - http://www.shelterexchange.org.",
     "Zeer lieve hond die graag een geweldig thuis zou willen hebben! Jimmy Choo, Border Collie Mix, is gedeeld van Shelter Exchange - http://www.shelterexchange.org."),
    
    ("Very sweet and loving and would love a good home! Dopey, Labrador Retriever Mix has been shared from Shelter Exchange - http://www.shelterexchange.org.",
     "Zeer lief en aanhankelijk en zou graag een goed thuis willen! Dopey, Labrador Retriever Mix, is gedeeld van Shelter Exchange - http://www.shelterexchange.org."),
    
    ("Sandy enjoys playing with and spending time with dogs. Most of all, she loves to snuggle and she chirps in her sleep! Best purr ever!",
     "Sandy houdt ervan om te spelen en tijd door te brengen met honden. Maar bovenal houdt ze ervan om te knuffelen en ze piept in haar slaap! Beste spin ooit!"),
    
    ("To learn more about Sansa, visit https://horseandridermatch.com/2018/06/08/sansa-2015-palomino-quarter-horse-filly-with-the-appalachian-trainer-face-off/",
     "Om meer te weten te komen over Sansa, bezoek https://horseandridermatch.com/2018/06/08/sansa-2015-palomino-quarter-horse-filly-with-the-appalachian-trainer-face-off/"),
    
    ("I am a fun, playful, 12-week-old handsome little man! Please visit me at Petsmart in Farmingdale or contact me at www.awaprescue.com",
     "Ik ben een leuke, speelse, 12 weken oude knappe kleine man! Bezoek me alsjeblieft bij Petsmart in Farmingdale of neem contact met me op via www.awaprescue.com"),
    
    ("Cute little Tobias was found all alone wandering in the campgrounds. Boy was he hungry! He is safe now and looking for his forever home!",
     "Schattige kleine Tobias werd helemaal alleen gevonden terwijl hij rondzwierf op de camping. Hij had honger! Hij is nu veilig en op zoek naar zijn eeuwige thuis!"),
    
    ("Male hooded rat. Hand tame and sweet. Will do well alone or with a cage mate. Most ages and colors of rats available for adoption.",
     "Mannelijke kaprat. Handtam en lief. Zal goed gedijen alleen of met een kooigenoot. De meeste leeftijden en kleuren ratten zijn beschikbaar voor adoptie.")
]


# Step 4: Test each case and print results
for en_sentence, expected_nl_sentence in test_cases:
    translation = translate_sentence(model, tokenizer, en_sentence)
    print(f"English: {en_sentence}")
    print(f"Generated Dutch Translation: {translation}")
