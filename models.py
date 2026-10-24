from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import Config

Base = declarative_base()

class User(Base):
    """User model for multi-user support"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    salary = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(Base):
    """Category model for expense classification"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    icon = Column(String(10), default='📦')
    color = Column(String(7), default='#C9ADA7')
    description = Column(Text)
    
    # Relationships
    expenses = relationship('Expense', backref='category', lazy=True)
    budgets = relationship('Budget', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Expense(Base):
    """Expense model for tracking daily expenses"""
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False, default=datetime.utcnow().date)
    description = Column(String(200))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'


class Budget(Base):
    """Budget model for setting spending limits"""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    monthly_limit = Column(Float, nullable=False)
    alerts_enabled = Column(Boolean, default=True)
    
    def __repr__(self):
        return f'<Budget {self.monthly_limit}>'


# Database setup
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database and create all tables"""
    Base.metadata.create_all(engine)

def get_session():
    """Get database session"""
    return SessionLocal()
