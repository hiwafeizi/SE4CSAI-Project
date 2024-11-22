import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from models import db, RequestLog, ResponseLog


# Configuration setup for the database
DATABASE_URI = os.environ.get('DATABASE_URL')

# Use SQLite as a fallback if DATABASE_URL is not set
if not DATABASE_URI:
    print("Warning: DATABASE_URL environment variable is not set. Using local SQLite database.")
    DATABASE_URI = "sqlite:///local_database.db"  # Set local SQLite database file path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)

# Route to process data from Interface Server
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_input = data.get('input')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Log the request
    request_log = RequestLog(input_text=user_input)
    db.session.add(request_log)
    db.session.commit()

    # Send data to AI Server
    response = requests.post('http://localhost:5002/run-ai', json={'input': user_input})
    if response.status_code == 200:
        ai_result = response.json().get('result')

        # Log the response
        response_log = ResponseLog(result_text=ai_result, request_id=request_log.id)
        db.session.add(response_log)
        db.session.commit()

        return jsonify({'result': ai_result}), 200
    else:
        return jsonify({'error': 'AI Server error'}), 500

if __name__ == '__main__':
    app.run(port=5001)
