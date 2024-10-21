from transformers import T5Tokenizer, T5ForConditionalGeneration

# Step 1: Load the saved model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('translation-model')
tokenizer = T5Tokenizer.from_pretrained('translation-model')

# Step 2: Define a function for translating sentences
def translate_sentence(model, tokenizer, sentence, max_length=50):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=max_length)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Step 3: Translate a new sentence
sentence = "Where is the nearest train station?"
translation = translate_sentence(model, tokenizer, sentence)
print(f"Translation: {translation}")