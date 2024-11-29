# routes.py
from flask import Blueprint, request, jsonify, current_app
from models import User, EnhancementRequest, TranslationRequest, db, PetDescriptionRequest
import requests
from werkzeug.security import generate_password_hash, check_password_hash

orchestrator = Blueprint('orchestrator', __name__)


@orchestrator.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email is already registered.'}), 400

        # Create a new user
        new_user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Signup successful.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orchestrator.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid email or password.'}), 401

        # Optionally return user data or a token
        return jsonify({'message': 'Login successful.', 'email': user.email}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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

        # Generate input text
        input_text = (
            f"Animal Type: {animal_type}. "
            f"Breed: {primary_breed or 'None'}. "
            f"Gender: {gender or 'None'}. "
            f"Color: {primary_color or 'None'}. "
            f"Size: {maturity_size or 'None'}. "
            f"Fur Length: {fur_length or 'None'}. "
            f"Vaccinated: {vaccinated or 'None'}. "
            f"Dewormed: {dewormed or 'None'}. "
            f"Sterilized: {sterilized or 'None'}. "
            f"Health: {health or 'None'}. "
            f"Quantity: {quantity or 'None'}. "
            f"Fee: ${fee or 'None'}."
        )

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
            fee=fee,
            input_text=input_text
        )
        db.session.add(new_request)
        db.session.commit()

        # Call the AI server to process the string
        ai_server_url = f"{current_app.config['AI_SERVER_URL']}/create"
        ai_response = requests.post(ai_server_url, json={"description": input_text})

        if ai_response.status_code == 200:
            result = ai_response.json().get('message', '')

            # Update the database with the result
            new_request.status = 'completed'
            new_request.result_text = result
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


@orchestrator.route('/history', methods=['GET'])
def get_history():
    try:
        # Query parameters for filtering (optional)
        request_type = request.args.get('type')  # create, translate, enhance
        limit = int(request.args.get('limit', 10))  # Number of records to fetch (default: 10)

        # Fetch records based on type
        if request_type == 'create':
            records = PetDescriptionRequest.query.order_by(PetDescriptionRequest.created_at.desc()).limit(limit).all()
        elif request_type == 'translate':
            records = TranslationRequest.query.order_by(TranslationRequest.created_at.desc()).limit(limit).all()
        elif request_type == 'enhance':
            records = EnhancementRequest.query.order_by(EnhancementRequest.created_at.desc()).limit(limit).all()
        else:
            # Fetch all types
            create_records = [
                {"record": record, "type": "create"}
                for record in PetDescriptionRequest.query.order_by(PetDescriptionRequest.created_at.desc()).limit(limit).all()
            ]
            translate_records = [
                {"record": record, "type": "translate"}
                for record in TranslationRequest.query.order_by(TranslationRequest.created_at.desc()).limit(limit).all()
            ]
            enhance_records = [
                {"record": record, "type": "enhance"}
                for record in EnhancementRequest.query.order_by(EnhancementRequest.created_at.desc()).limit(limit).all()
            ]
            records = create_records + translate_records + enhance_records

        # Serialize the records
        if request_type:
            results = [
                {
                    "id": record.id,
                    "type": request_type,
                    "input_text": getattr(record, 'input_text', None),
                    "result_text": getattr(record, 'result_text', None),
                    "status": record.status,
                    "created_at": record.created_at,
                }
                for record in records
            ]
        else:
            results = [
                {
                    "id": item["record"].id,
                    "type": item["type"],
                    "input_text": getattr(item["record"], 'input_text', None),
                    "result_text": getattr(item["record"], 'result_text', None),
                    "status": item["record"].status,
                    "created_at": item["record"].created_at,
                }
                for item in records
            ]

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orchestrator.route('/delete_record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    try:
        # Determine which table the record belongs to based on its ID
        record_type = request.args.get('type')  # 'create', 'translate', 'enhance'
        if record_type == 'create':
            record = PetDescriptionRequest.query.get(record_id)
        elif record_type == 'translate':
            record = TranslationRequest.query.get(record_id)
        elif record_type == 'enhance':
            record = EnhancementRequest.query.get(record_id)
        else:
            return jsonify({'error': 'Invalid record type.'}), 400

        if not record:
            return jsonify({'error': 'Record not found.'}), 404

        # Delete the record
        db.session.delete(record)
        db.session.commit()

        return jsonify({'message': 'Record deleted successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orchestrator.route('/clear_records', methods=['POST'])
def clear_records():
    try:
        # Clear all records from the three tables
        num_create_deleted = db.session.query(PetDescriptionRequest).delete()
        num_translate_deleted = db.session.query(TranslationRequest).delete()
        num_enhance_deleted = db.session.query(EnhancementRequest).delete()

        # Commit the changes to the database
        db.session.commit()

        # Return success message
        return jsonify({
            "message": "All records have been deleted successfully.",
            "details": {
                "create_deleted": num_create_deleted,
                "translate_deleted": num_translate_deleted,
                "enhance_deleted": num_enhance_deleted
            }
        }), 200
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
