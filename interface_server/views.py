from flask import Blueprint, jsonify, render_template, redirect, request, url_for, flash

app_views = Blueprint('app_views', __name__)


@app_views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app_views.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')

@app_views.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')

@app_views.route('/features', methods=['GET'])
def features():
    return render_template('features.html') 

# Route for "Create Descriptions"
@app_views.route('/create', methods=['POST'])
def create_description():
    data = request.json  # Parse the JSON request data
    animal_type = data.get('animal_type', 'Unknown')
    primary_breed = data.get('primary_breed', 'Unknown')
    gender = data.get('gender', 'Unknown')
    primary_color = data.get('primary_color', 'Unknown')
    maturity_size = data.get('maturity_size', 'Unknown')
    fur_length = data.get('fur_length', 'Unknown')
    vaccinated = data.get('vaccinated', 'Unknown')
    dewormed = data.get('dewormed', 'Unknown')
    sterilized = data.get('sterilized', 'Unknown')
    health = data.get('health', 'Unknown')
    quantity = data.get('quantity', 1)
    fee = data.get('fee', 0)

    # Generate a sample description based on the provided data
    description = (
        f"This {animal_type} is a {primary_breed} with {primary_color} fur. "
        f"It is {gender.lower()}, {maturity_size.lower()} in size, and has {fur_length.lower()} fur. "
        f"Health status: {health}. Vaccinated: {vaccinated}. Dewormed: {dewormed}. "
        f"Sterilized: {sterilized}. Quantity: {quantity}. Adoption fee: ${fee}."
    )

    return jsonify({'message': description})

@app_views.route('/translate', methods=['POST'])
def translate_description():
    data = request.json  # Parse the JSON request data
    print("Received data:", data)  # Debug log

    if not data:
        return jsonify({'message': 'Invalid request: No data provided.'}), 400

    description = data.get('translate_input', '')

    if not description:
        return jsonify({'message': 'Invalid request: Missing translate_input field.'}), 400

    # Simulate a translation (placeholder logic)
    translated_description = description[::-1]

    return jsonify({'message': f'Translated description: {translated_description}'})


# Route for "Enhance Descriptions"
@app_views.route('/enhance', methods=['POST'])
def enhance_description():
    data = request.json  # Parse the JSON request data
    description = data.get('enhance_input', '')

    # Simulate enhancement by capitalizing the first letter of each sentence
    enhanced_description = '. '.join(sentence.capitalize() for sentence in description.split('. '))

    return jsonify({'message': f'Enhanced description: {enhanced_description}'})
