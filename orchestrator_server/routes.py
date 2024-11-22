# routes.py
from flask import Blueprint, request, jsonify, current_app
from models import db, PetDescriptionRequest
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

        # Save the request to the database
        new_request = PetDescriptionRequest(
            animal_type=animal_type,
            primary_breed=data.get('primary_breed'),
            gender=data.get('gender'),
            primary_color=data.get('primary_color'),
            maturity_size=data.get('maturity_size'),
            fur_length=data.get('fur_length'),
            vaccinated=data.get('vaccinated'),
            dewormed=data.get('dewormed'),
            sterilized=data.get('sterilized'),
            health=data.get('health'),
            quantity=data.get('quantity'),
            fee=data.get('fee')
        )
        db.session.add(new_request)
        db.session.commit()

        # Prepare payload for AI server
        ai_payload = {
            'animal_type': new_request.animal_type,
            'primary_breed': new_request.primary_breed or '',
            'gender': new_request.gender or '',
            'primary_color': new_request.primary_color or '',
            'maturity_size': new_request.maturity_size or '',
            'fur_length': new_request.fur_length or '',
            'vaccinated': new_request.vaccinated or '',
            'dewormed': new_request.dewormed or '',
            'sterilized': new_request.sterilized or '',
            'health': new_request.health or '',
            'quantity': new_request.quantity or '',
            'fee': new_request.fee or ''
        }

        # Call the AI server to process the request
        ai_server_url = f"{current_app.config['AI_SERVER_URL']}/create"
        ai_response = requests.post(ai_server_url, json=ai_payload)

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
