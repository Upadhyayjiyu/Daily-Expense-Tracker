from models import Base, User, Category, Expense, Budget, engine, get_session
from config import Config
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with tables and default data"""
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("✓ Tables created successfully")
    
    session = get_session()
    
    try:
        # Create default categories
        print("\nAdding default categories...")
        for cat_data in Config.DEFAULT_CATEGORIES:
            existing = session.query(Category).filter_by(name=cat_data['name']).first()
            if not existing:
                category = Category(
                    name=cat_data['name'],
                    icon=cat_data['icon'],
                    color=cat_data['color']
                )
                session.add(category)
                print(f"  ✓ Added category: {cat_data['icon']} {cat_data['name']}")
        
        session.commit()
        print("✓ Categories added successfully")
        
        # Create a default user
        print("\nCreating default user...")
        existing_user = session.query(User).filter_by(username='demo_user').first()
        if not existing_user:
            user = User(
                username='demo_user',
                email='demo@expense-tracker.com',
                salary=50000.0
            )
            session.add(user)
            session.commit()
            print(f"✓ Created user: {user.username} (ID: {user.id})")
            
            # Create sample expenses for the demo user
            print("\nAdding sample expenses for demonstration...")
            categories = session.query(Category).all()
            
            # Generate expenses for the last 30 days
            for i in range(30):
                expense_date = datetime.now().date() - timedelta(days=i)
                num_expenses = random.randint(1, 3)
                
                for _ in range(num_expenses):
                    category = random.choice(categories)
                    amount = round(random.uniform(50, 1500), 2)
                    
                    expense = Expense(
                        user_id=user.id,
                        category_id=category.id,
                        amount=amount,
                        date=expense_date,
                        description=f"Sample {category.name} expense",
                        notes=f"Auto-generated sample data"
                    )
                    session.add(expense)
            
            session.commit()
            print(f"✓ Added sample expenses for the last 30 days")
            
            # Create sample budgets
            print("\nCreating sample budgets...")
            food_cat = session.query(Category).filter_by(name='Food').first()
            travel_cat = session.query(Category).filter_by(name='Travel').first()
            
            if food_cat:
                budget1 = Budget(
                    user_id=user.id,
                    category_id=food_cat.id,
                    monthly_limit=10000.0,
                    alerts_enabled=True
                )
                session.add(budget1)
            
            if travel_cat:
                budget2 = Budget(
                    user_id=user.id,
                    category_id=travel_cat.id,
                    monthly_limit=5000.0,
                    alerts_enabled=True
                )
                session.add(budget2)
            
            session.commit()
            print("✓ Sample budgets created")
        else:
            print(f"✓ User already exists: {existing_user.username}")
        
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE!")
        print("="*50)
        print("\nDefault credentials:")
        print("  Username: demo_user")
        print("  Email: demo@expense-tracker.com")
        print("\nYou can now run: python app.py")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Error during initialization: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    init_database()
