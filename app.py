from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a professional customer service representative for BRAVERMAN, 
                    a luxury jewelry store. You specialize in engagement rings, wedding rings, and fine jewelry. 
                    Maintain a professional, courteous tone and provide detailed information about our products, 
                    customization options, and services. If asked about prices, provide general ranges and 
                    encourage customers to visit our website or contact us for specific quotes."""
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "error": "I apologize, but I'm having trouble processing your request. Please try again or contact our support team directly."
        }), 500

# Update the last section
if __name__ == '__main__':
    # Use production server when deployed, development server locally
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)