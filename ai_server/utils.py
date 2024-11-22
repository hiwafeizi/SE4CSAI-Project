# Import the functions from their respective files
from create import generate_pet_description as form2text_generate_description
from translate import translate_english_to_dutch as translate
from enhance import enhance_description as enhance

# Function to generate a description from form input
def generate_description(description):
    """
    Generate a description by calling the function from form2text.py.
    """
    return form2text_generate_description(description)

# Function to translate text
def translate_text(text):
    """
    Translate text by calling the function from translate.py.
    """
    return translate(text)

# Function to enhance text
def enhance_text(text):
    """
    Enhance text by calling the function from enhance.py.
    """
    return enhance(text)
