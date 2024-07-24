from flask import Flask, request, jsonify
from flask_cors import CORS
from back.chatbot import predict_class

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['message']
    response_text = predict_class(text)
    return jsonify({'answer': response_text})

if __name__ == '__main__':
    app.run(debug=True)
