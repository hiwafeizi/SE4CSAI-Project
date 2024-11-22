from transformers import MarianMTModel, MarianTokenizer

# Step 1: Load the saved MarianMT model and tokenizer
model = MarianMTModel.from_pretrained('AI/translate')
tokenizer = MarianTokenizer.from_pretrained('AI/translate')

# Step 2: Define a function for translating sentences
def translate_sentence(model, tokenizer, sentence, max_length=200):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=max_length)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Test cases
test_cases = [
    (
        "Energetic and loyal Labrador looking for a loving home. Black, large-sized with short fur, vaccinated and dewormed. Needs a family to give him the attention he deserves. Fee: $100.",
        "Energieke en loyale Labrador op zoek naar een liefdevol thuis. Zwart, groot met korte vacht, gevaccineerd en ontwormd. Heeft een familie nodig die hem de aandacht geeft die hij verdient. Kosten: $100."
    ),
    (
        "Beautiful white Persian cat with long fur and a gentle temperament. Spayed and ready for adoption despite a minor injury. Looking for a caring home. Adoption fee: $50.",
        "Mooie witte Perzische kat met lange vacht en een zacht temperament. Gesteriliseerd en klaar voor adoptie ondanks een kleine blessure. Op zoek naar een liefdevol thuis. Adoptiekosten: $50."
    ),
    (
        "Friendly and healthy Beagle, brown and white, ready for adoption. Medium-sized with short fur, fully vaccinated, dewormed, and neutered. Adoption fee: $75.",
        "Vriendelijke en gezonde Beagle, bruin en wit, klaar voor adoptie. Middelgroot met korte vacht, volledig gevaccineerd, ontwormd en gecastreerd. Adoptiekosten: $75."
    ),
    (
        "Two adorable Siamese cats, grey with medium-length fur. These small, healthy cats are playful and looking for a home. Free to a loving family.",
        "Twee schattige Siamese katten, grijs met middellange vacht. Deze kleine, gezonde katten zijn speels en op zoek naar een thuis. Gratis voor een liefdevolle familie."
    ),
    (
        "Special needs Poodle with long white fur, recently spayed. Needs attentive care due to a serious injury. Adoption fee: $30.",
        "Speciale zorg nodig voor Poodle met lange witte vacht, recentelijk gesteriliseerd. Heeft zorg nodig vanwege een ernstige blessure. Adoptiekosten: $30."
    )
]


# # Step 4: Test each case and print results
# for en_sentence, expected_nl_sentence in test_cases:
#     translation = translate_sentence(model, tokenizer, en_sentence)
#     print(f"English: {en_sentence}")
#     print(f"Generated Dutch Translation: {translation}")

from nltk.translate.bleu_score import sentence_bleu

def evaluate_with_bleu(model, tokenizer, test_cases):
    scores = []
    for input_text, expected_translation in test_cases:
        generated_translation = translate_sentence(model, tokenizer, input_text)
        reference = [expected_translation.split()]
        candidate = generated_translation.split()
        bleu_score = sentence_bleu(reference, candidate)
        scores.append(bleu_score)
        print(f"Input: {input_text}")
        print(f"Generated: {generated_translation}")
        print(f"Expected: {expected_translation}")
        print(f"BLEU Score: {bleu_score}\n")
    
    avg_bleu = sum(scores) / len(scores)
    print(f"Average BLEU Score: {avg_bleu}")

# Run BLEU evaluation
evaluate_with_bleu(model, tokenizer, test_cases)
