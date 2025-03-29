import sqlite3
import json
from datetime import datetime

def get_db():
    conn = sqlite3.connect('diet_bot.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
   
    c.execute('''
        CREATE TABLE IF NOT EXISTS diet_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            keywords TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES diet_categories (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            recommendation_id INTEGER,
            FOREIGN KEY (recommendation_id) REFERENCES recommendations (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            calories INTEGER,
            meal_plan_id INTEGER,
            FOREIGN KEY (meal_plan_id) REFERENCES meal_plans (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount TEXT,
            meal_id INTEGER,
            FOREIGN KEY (meal_id) REFERENCES meals (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES diet_categories (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_categories():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM diet_categories')
    categories = c.fetchall()
    conn.close()
    return categories

def get_recommendations_by_category(category_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM recommendations WHERE category_id = ?', (category_id,))
    recommendations = c.fetchall()
    conn.close()
    return recommendations

def add_interaction(user_message, bot_response, category_id=None):
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_interactions (user_message, bot_response, category_id)
        VALUES (?, ?, ?)
    ''', (user_message, json.dumps(bot_response), category_id))
    conn.commit()
    conn.close() 