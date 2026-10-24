import os

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Database
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "expense_tracker.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Default categories with icons and colors
    DEFAULT_CATEGORIES = [
        {'name': 'Food', 'icon': '🍔', 'color': '#FF6B6B'},
        {'name': 'Travel', 'icon': '🚗', 'color': '#4ECDC4'},
        {'name': 'Bills', 'icon': '📄', 'color': '#95E1D3'},
        {'name': 'Shopping', 'icon': '🛍️', 'color': '#F38181'},
        {'name': 'Entertainment', 'icon': '🎬', 'color': '#AA96DA'},
        {'name': 'Groceries', 'icon': '🛒', 'color': '#FCBAD3'},
        {'name': 'Utilities', 'icon': '⚡', 'color': '#A8D8EA'},
        {'name': 'Health', 'icon': '🏥', 'color': '#FFD93D'},
        {'name': 'Household', 'icon': '🏠', 'color': '#6BCB77'},
        {'name': 'Education', 'icon': '📚', 'color': '#4D96FF'},
        {'name': 'Rent', 'icon': '🔑', 'color': '#FF9A8B'},
        {'name': 'Other', 'icon': '📦', 'color': '#C9ADA7'},
    ]
    
    # Essential household bills
    ESSENTIAL_BILLS = ['Rent', 'Utilities', 'Groceries', 'Bills']
