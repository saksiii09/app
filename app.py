from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Store API key in environment variables

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 150
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200 and 'choices' in response_data:
            ai_response = response_data['choices'][0].get('text', 'No response received.')
        else:
            ai_response = "Sorry, no valid response from DeepSeek."

    except requests.exceptions.RequestException as e:
        ai_response = "Request failed: " + str(e)

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)  # Change to debug=False in production
