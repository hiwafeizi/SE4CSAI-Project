# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 09:54:20 2024

@author: stand
"""

import pandas as pd
import unittest

import sys
import os
import torch

# Add the directory containing form2text.py to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from form2text import prepare_form2description_data

from unittest.mock import patch, MagicMock
from sampling import analyze_data
from translate_usage import translate_sentence
from enhance_test import generate_enhancement

from transformers import T5ForConditionalGeneration, T5Tokenizer
from form2text_usage import generate_description, load_model


class TestForm2text(unittest.TestCase):
    def setup(self):
        self.data = pd.DataFrame({
            "Type": ["Dog", "Cat"], 
            "Primary Breed": ["Labrador", "Siamese"], 
            "Gender": ["Female", "Male"], 
            "Primary Color": ["White", "Grey"],
            "Maturity Size": ["Large", "Small"], 
            "Fur Length": ["Short", "Short"], 
            "Vaccinated": ["Yes", "No"], 
            "Dewormed": ["Yes", "No"],
            "Sterilized": ["Yes", "No"], 
            "Health": ["Healthy", "Healthy"],
            "Quantity": [2, 1],
            "Fee": [300, 60],
            "Description": ["Active Labradors", "Calm Siamese"]
        })
    
    def test_prepare_form2description(self):
        prepared_data = prepare_form2description_data(self.data)
        
        #expected input all rows except description (which is output)
        expected_input = [
            "Type: Dog, Primary Breed: Labrador, Gender: Female, Primary Color: White, "
            "Maturity Size: Large, Fur Length: Short, Vaccinated: Yes, Dewormed: Yes, "
            "Sterilized: Yes, Health: Healthy, Quantity: 2, Fee: 300",
            
            "Type: Cat, Primary Breed: Siamese, Gender: Male, Primary Color: Grey, "
            "Maturity Size: Small, Fur Length: Short, Vaccinated: No, Dewormed: No, "
            "Sterilized: No, Health: Healthy, Quantity: 1, Fee: 60"
        ]
        
        self.assertEqual(prepared_data['input'].tolist(), expected_input)
        self.assertEqual(prepared_data['output'].tolist(), self.data['Description'].tolist())
        
class TestAnalyzedata(unittest.TestCase):
    @patch('os.makedirs')
    @patch('pandas.DataFrame.to_csv')
    def test_analyze_data(self, mock_to_csv, mock_makedirs):
       mock_data = pd.DataFrame({
           'country': ['Country1', 'Country2'],
           'color_code': ['Red', 'Blue'],
           'pet': ['Dog', 'Cat'],
           'age': [2, 3],
           'gender': ['Male', 'Female'],
           'size': ['Medium', 'Small'],
           'photos': [1, 2],
           'text': ['Description 1', 'Description 2']
       })
       
        
       analyze_data(mock_data)

       # Check if the os.makedirs was called to create the directory
       mock_makedirs.assert_called_with(os.path.dirname("data/form2description_reduced.csv"), exist_ok=True)
       
       # Check if to_csv was called with the correct path
       mock_to_csv.assert_called_with("data/form2description_reduced.csv", index=False)

class TestTranslate(unittest.TestCase):
    
    def test_translate_sentence(self):
        #input
        input_sentence = "Energetic and loyal Labrador looking for a loving home. Black, large-sized with short fur, vaccinated and dewormed. Needs a family to give him the attention he deserves. Fee: $100."
        #expected output
        output_sentence = "Energieke en loyale Labrador op zoek naar een liefdevol thuis. Zwart, groot met korte vacht, gevaccineerd en ontwormd. Heeft een familie nodig die hem de aandacht geeft die hij verdient. Kosten: $100."
        
        #mock the model and tokenizer
        model_mock = MagicMock()
        tokenizer_mock = MagicMock()
        
        # Mock the model behavior
        model_mock.generate.return_value = [[101, 102, 103, 104]]  # Example mock output token ids

        # Call the function to test
        translation = translate_sentence(model_mock, tokenizer_mock, input_sentence)
        
        # Assertions to verify the results
        self.assertEqual(translation, output_sentence)  # Check if the translation matches the expected
        
        # Verify that the tokenizer and model methods were called correctly
        tokenizer_mock.assert_called_once_with(input_sentence, return_tensors="pt")
        model_mock.generate.assert_called_once_with([101, 102, 103], max_length=200)
        tokenizer_mock.decode.assert_called_once_with([101, 102, 103, 104], skip_special_tokens=True)

class TestEnhance(unittest.TestCase):

    @patch('enhance_test.model.generate')  # Mock the model's generate method
    @patch('enhance_test.tokenizer.decode')  # Mock the tokenizer's decode method
    def test_generate_enhancement(self, mock_decode, mock_generate):
        # Define mock behavior
        mock_generate.return_value = torch.tensor([[101, 102, 103, 104]])  # Mock tokenized output
        mock_decode.return_value = "Enhanced description text."

        # Test input text
        input_text = "Nibble is an energetic, playful kitten, about 3 months old. I’m seeking a responsible new home for him due to limited space and resources."
        
        # Call the function with mock values
        enhanced_text = generate_enhancement(input_text)

        # Assert the function returns the expected output
        self.assertEqual(enhanced_text, "Enhanced description text.")
        
        # Assert that the model's generate method was called with the correct parameters
        mock_generate.assert_called_once()
        
        # Assert that the tokenizer's decode method was called to process the generated tokens
        mock_decode.assert_called_once_with([101, 102, 103, 104], skip_special_tokens=True)    
        
class TestForm2textusage(unittest.TestCase):
    
    @patch('form2text_usage.T5ForConditionalGeneration.from_pretrained')
    @patch('form2text_usage.T5Tokenizer.from_pretrained')
    def test_generate_description(self, mock_tokenizer, mock_model):
        # Mock tokenizer and model
        mock_tokenizer.return_value = T5Tokenizer.from_pretrained('t5-small')
        mock_model.return_value = T5ForConditionalGeneration.from_pretrained('t5-small')

        tokenizer, model = load_model('t5-small')  # Mocked model and tokenizer

        # Test case data
        form_input = "Type: Dog, Primary Breed: Labrador, Gender: Male, Primary Color: Black, Maturity Size: Large, Fur Length: Short, Vaccinated: Yes, Dewormed: Yes, Sterilized: No, Health: Healthy, Quantity: 1, Fee: 100"
        expected_description = "Energetic and loyal Labrador looking for a loving home. Black, large-sized with short fur, vaccinated and dewormed. Needs a family to give him the attention he deserves. Fee: $100."

        # Mock model's generate method
        with patch.object(model, 'generate') as mock_generate:
            mock_generate.return_value = torch.tensor([[101, 102, 103, 104]])  # Example tokenized output

            # Mock tokenizer's decode method
            with patch.object(tokenizer, 'decode') as mock_decode:
                mock_decode.return_value = expected_description  # Mock the decoded output
                
                # Call the function
                generated_description = generate_description(tokenizer, model, form_input)

                # Assert that the generated description matches the expected one
                self.assertEqual(generated_description, expected_description)

                # Ensure generate was called
                mock_generate.assert_called_once()

                # Ensure decode was called with the right parameters
                mock_decode.assert_called_once_with([101, 102, 103, 104], skip_special_tokens=True)

    
if __name__ == "__main__": 
    unittest.main()