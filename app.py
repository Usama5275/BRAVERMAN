from flask import Flask, render_template, request, jsonify
import os
import openai

# Create Flask app
app = Flask(__name__)

# Configure environment-specific settings
if os.getenv('PRODUCTION'):
    # Production settings (PythonAnywhere)
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    # Development settings (Local)
    from dotenv import load_dotenv
    load_dotenv()
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
                    a luxury jewelry store. You specialize in fine jewelry with expertise in the following categories:
                    
                    ENGAGEMENT RINGS:
                    - Salt and Pepper Diamond Engagement Rings
                    - Moissanite Engagement Rings
                    - Lab Grown Diamond Engagement Rings
                    - Gemstone Engagement Rings
                    - Bridal Ring Set
                    - Teal Sapphire Engagement Rings
                    - Custom Design Your Engagement Ring
                    
                    WOMEN'S WEDDING RINGS:
                    - Diamond Wedding Rings
                    - Salt and Pepper Diamond Wedding Rings
                    - Moissanite Wedding Rings
                    - Gemstone Wedding Rings
                    
                    MEN'S WEDDING BANDS:
                    - Gold Wedding Bands
                    - Platinum Wedding Bands
                    - Tungsten Wedding Bands
                    - Titanium Wedding Bands
                    - Black Zirconium Wedding Bands
                    
                    CUSTOM DESIGN SERVICES:
                    - Custom Design Your Wedding Ring
                    
                    Provide detailed information about our materials, craftsmanship, and customization options.
                    When discussing prices, provide general ranges and encourage customers to contact us for specific quotes.
                    Maintain a professional, courteous tone and emphasize our commitment to quality and customer satisfaction.
                    
                    If customers have specific questions about shipping, returns, or sizing, provide general policies
                    and invite them to call us at 1-800-990-3822 for personalized assistance."""
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
    # Development server settings
    app.run(host='0.0.0.0', port=8000, debug=True)