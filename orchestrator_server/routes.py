# routes.py
from flask import Blueprint, request, jsonify, current_app
from models import EnhancementRequest, TranslationRequest, db, PetDescriptionRequest
import requests

orchestrator = Blueprint('orchestrator', __name__)

@orchestrator.route('/create', methods=['POST'])
def create_description_request():
    try:
        # Parse incoming data
        data = request.json

        # Validate the required field
        animal_type = data.get('animal_type')
        if not animal_type:
            return jsonify({'error': 'The animal_type field is required.'}), 400

        # Process optional fields with default values and type conversion
        def parse_field(value, default, cast_type):
            try:
                return cast_type(value) if value else default
            except ValueError:
                return default

        primary_breed = data.get('primary_breed', None)
        gender = data.get('gender', None)
        primary_color = data.get('primary_color', None)
        maturity_size = data.get('maturity_size', None)
        fur_length = data.get('fur_length', None)
        vaccinated = data.get('vaccinated', None)
        dewormed = data.get('dewormed', None)
        sterilized = data.get('sterilized', None)
        health = data.get('health', None)

        quantity = parse_field(data.get('quantity'), 1, int)  # Default to 1 if empty or invalid
        fee = parse_field(data.get('fee'), 0.0, float)        # Default to 0.0 if empty or invalid

        # Save the request to the database
        new_request = PetDescriptionRequest(
            animal_type=animal_type,
            primary_breed=primary_breed,
            gender=gender,
            primary_color=primary_color,
            maturity_size=maturity_size,
            fur_length=fur_length,
            vaccinated=vaccinated,
            dewormed=dewormed,
            sterilized=sterilized,
            health=health,
            quantity=quantity,
            fee=fee
        )
        db.session.add(new_request)
        db.session.commit()

        # Process data into a string format
        description_string = (
            f"Animal Type: {new_request.animal_type}. "
            f"Breed: {new_request.primary_breed or 'None'}. "
            f"Gender: {new_request.gender or 'None'}. "
            f"Color: {new_request.primary_color or 'None'}. "
            f"Size: {new_request.maturity_size or 'None'}. "
            f"Fur Length: {new_request.fur_length or 'None'}. "
            f"Vaccinated: {new_request.vaccinated or 'None'}. "
            f"Dewormed: {new_request.dewormed or 'None'}. "
            f"Sterilized: {new_request.sterilized or 'None'}. "
            f"Health: {new_request.health or 'None'}. "
            f"Quantity: {new_request.quantity or 'None'}. "
            f"Fee: ${new_request.fee or 'None'}."
        )

        # Call the AI server to process the string
        ai_server_url = f"{current_app.config['AI_SERVER_URL']}/create"
        ai_response = requests.post(ai_server_url, json={"description": description_string})

        if ai_response.status_code == 200:
            result = ai_response.json().get('message', '')

            # Update the database with the result
            new_request.status = 'completed'
            new_request.result = result
            db.session.commit()

            return jsonify({'message': 'Request processed successfully', 'result': result})
        else:
            new_request.status = 'failed'
            db.session.commit()
            return jsonify({'error': 'Failed to process the request via AI server'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orchestrator.route('/translate', methods=['POST'])
def translate_description_request():
    try:
        # Parse incoming data
        data = request.json
        description = data.get('translate_input')
        if not description:
            return jsonify({'error': 'The translate_input field is required.'}), 400

        # Save the request to the database
        translation_request = TranslationRequest(
            input_text=description,
            status='processing'
        )
        db.session.add(translation_request)
        db.session.commit()

        # Call the AI server for translation
        ai_server_url = f"{current_app.config['AI_SERVER_URL']}/translate"
        ai_response = requests.post(ai_server_url, json={"text": description})

        if ai_response.status_code == 200:
            translated_text = ai_response.json().get('message', '')

            # Update the database with the result
            translation_request.status = 'completed'
            translation_request.result_text = translated_text
            db.session.commit()

            return jsonify({'message': 'Request processed successfully', 'result': translated_text})
        else:
            translation_request.status = 'failed'
            db.session.commit()
            return jsonify({'error': 'Failed to process the request via AI server'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orchestrator.route('/enhance', methods=['POST'])
def enhance_description_request():
    try:
        # Parse incoming data
        data = request.json
        description = data.get('enhance_input')
        if not description:
            return jsonify({'error': 'The enhance_input field is required.'}), 400

        # Save the request to the database
        enhancement_request = EnhancementRequest(
            input_text=description,
            status='processing'
        )
        db.session.add(enhancement_request)
        db.session.commit()

        # Call the AI server for enhancement
        ai_server_url = f"{current_app.config['AI_SERVER_URL']}/enhance"
        ai_response = requests.post(ai_server_url, json={"text": description})

        if ai_response.status_code == 200:
            enhanced_text = ai_response.json().get('message', '')

            # Update the database with the result
            enhancement_request.status = 'completed'
            enhancement_request.result_text = enhanced_text
            db.session.commit()

            return jsonify({'message': 'Request processed successfully', 'result': enhanced_text})
        else:
            enhancement_request.status = 'failed'
            db.session.commit()
            return jsonify({'error': 'Failed to process the request via AI server'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
