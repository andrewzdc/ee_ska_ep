from flask import Flask, request, jsonify
from datetime import datetime
from urllib.parse import unquote
import json

app = Flask(__name__)
data_store = []  # Temporary in-memory store

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        json_data = request.get_json()
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'fields': [{'field_name': k, 'field_value': v} for k, v in json_data.items()]
        }
        data_store.append(entry)
        return jsonify({"status": "stored"}), 200
    return jsonify({"status": "error", "message": "Invalid JSON"}), 400

@app.route('/webhook-get', methods=['GET'])
def webhook_get():
    data = request.args.to_dict()
    
    if 'spyop_json' in data:
        try:
            decoded_str = unquote(data['spyop_json'])
            spyop_data = json.loads(decoded_str)
            data.update(spyop_data)
        except Exception as e:
            return jsonify({"status": "error", "message": f"Failed to decode spyop_json: {str(e)}"}), 400

    # Format into your expected structure with timestamp and fields
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'fields': [{'field_name': k, 'field_value': v} for k, v in data.items()]
    }

    data_store.append(entry)
    return jsonify(entry), 200

@app.route('/get-latest', methods=['GET'])
def get_latest():
    if data_store:
        # Return and clear all stored entries
        latest_data = list(data_store)
        data_store.clear()
        return jsonify(latest_data), 200
    return jsonify([]), 200

if __name__ == '__main__':
    app.run()
