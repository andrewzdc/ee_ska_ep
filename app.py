from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
        parsed_data = [{'field_name': k, 'field_value': v} for k, v in data.items()]
        print("Received JSON:", parsed_data)
        return jsonify({"status": "received"}), 200
    return jsonify({"status": "error", "message": "Invalid JSON"}), 400

if __name__ == '__main__':
    app.run()