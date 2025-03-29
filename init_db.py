from models import init_db, get_db
import json

def populate_db():
    conn = get_db()
    c = conn.cursor()
    
    
    categories = {
        "weight_loss": {
            "name": "Weight Loss",
            "description": "Diet recommendations for weight loss",
            "keywords": json.dumps(["lose weight", "slim down", "weight loss", "fat loss"]),
            "recommendations": [
                "Focus on calorie deficit - consume fewer calories than you burn",
                "Include lean proteins like chicken, fish, and tofu",
                "Eat plenty of vegetables and fruits",
                "Choose whole grains over refined grains",
                "Stay hydrated with water",
                "Limit processed foods and sugary drinks"
            ]
        },
        "muscle_gain": {
            "name": "Muscle Gain",
            "description": "Diet recommendations for muscle building",
            "keywords": json.dumps(["build muscle", "gain muscle", "strength", "bulk up"]),
            "recommendations": [
                "Increase protein intake (1.6-2.2g per kg of body weight)",
                "Eat in a calorie surplus",
                "Include complex carbohydrates",
                "Consume healthy fats",
                "Eat frequent meals throughout the day",
                "Focus on nutrient-dense foods"
            ]
        },
        "healthy_eating": {
            "name": "Healthy Eating",
            "description": "General healthy eating guidelines",
            "keywords": json.dumps(["healthy diet", "balanced diet", "nutrition", "healthy eating"]),
            "recommendations": [
                "Eat a variety of colorful fruits and vegetables",
                "Include whole grains in your diet",
                "Choose lean proteins",
                "Limit saturated fats and trans fats",
                "Reduce sodium intake",
                "Stay hydrated"
            ]
        },
        "vegetarian": {
            "name": "Vegetarian",
            "description": "Vegetarian diet recommendations",
            "keywords": json.dumps(["vegetarian", "plant-based", "meat-free"]),
            "recommendations": [
                "Include plant-based proteins (legumes, tofu, tempeh)",
                "Eat a variety of vegetables and fruits",
                "Include whole grains",
                "Consume dairy or dairy alternatives",
                "Ensure adequate iron intake from plant sources",
                "Include nuts and seeds for healthy fats"
            ]
        }
    }
    
    for category_data in categories.values():
        c.execute('''
            INSERT INTO diet_categories (name, description, keywords)
            VALUES (?, ?, ?)
        ''', (category_data["name"], category_data["description"], category_data["keywords"]))
        category_id = c.lastrowid
        
        for rec_text in category_data["recommendations"]:
            c.execute('''
                INSERT INTO recommendations (text, category_id)
                VALUES (?, ?)
            ''', (rec_text, category_id))
            recommendation_id = c.lastrowid
            
            
            c.execute('''
                INSERT INTO meal_plans (name, description, recommendation_id)
                VALUES (?, ?, ?)
            ''', (f"Sample {category_data['name']} Meal Plan", f"Meal plan supporting: {rec_text}", recommendation_id))
            meal_plan_id = c.lastrowid
            
            
            meals = [
                {
                    "name": "Breakfast",
                    "description": "Healthy breakfast option",
                    "calories": 400,
                    "ingredients": [
                        {"name": "Oatmeal", "amount": "1 cup"},
                        {"name": "Banana", "amount": "1 medium"},
                        {"name": "Almonds", "amount": "10 pieces"}
                    ]
                },
                {
                    "name": "Lunch",
                    "description": "Nutritious lunch option",
                    "calories": 600,
                    "ingredients": [
                        {"name": "Grilled Chicken", "amount": "150g"},
                        {"name": "Brown Rice", "amount": "1 cup"},
                        {"name": "Mixed Vegetables", "amount": "1 cup"}
                    ]
                }
            ]
            
            for meal_data in meals:
                c.execute('''
                    INSERT INTO meals (name, description, calories, meal_plan_id)
                    VALUES (?, ?, ?, ?)
                ''', (meal_data["name"], meal_data["description"], meal_data["calories"], meal_plan_id))
                meal_id = c.lastrowid
                
                for ingredient_data in meal_data["ingredients"]:
                    c.execute('''
                        INSERT INTO ingredients (name, amount, meal_id)
                        VALUES (?, ?, ?)
                    ''', (ingredient_data["name"], ingredient_data["amount"], meal_id))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    populate_db()
    print("Database initialized with sample data!") 