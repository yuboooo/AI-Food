from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes to allow requests from React frontend
CORS(app)

# Test route
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello from Flask!, testtest"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)