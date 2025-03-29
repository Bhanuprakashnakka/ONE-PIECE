from flask import Flask, render_template, request, jsonify
from models import get_categories, get_recommendations_by_category, add_interaction
import json

app = Flask(__name__)

def get_recommendations(user_input):
    user_input = user_input.lower()
    recommendations = []
    matched_category = None
    
    
    categories = get_categories()
    for category in categories:
        keywords = json.loads(category['keywords'])
        if any(keyword in user_input for keyword in keywords):
            matched_category = category
            
            category_recommendations = get_recommendations_by_category(category['id'])
            recommendations.extend([rec['text'] for rec in category_recommendations])
            break
    
    if not recommendations:
        recommendations = [
            "I'm not sure about your specific dietary needs. Could you please provide more details about your goals?",
            "Are you looking to lose weight, gain muscle, or maintain a healthy diet?",
            "Do you have any specific dietary restrictions?"
        ]
    
    
    add_interaction(user_input, recommendations, matched_category['id'] if matched_category else None)
    
    return recommendations

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    recommendations = get_recommendations(user_message)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True) 