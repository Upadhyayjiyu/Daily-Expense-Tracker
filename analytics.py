from models import get_session, Expense, Category, User, Budget
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

class ExpenseAnalytics:
    """Analytics engine for expense tracking"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()
    
    def get_category_wise_expenses(self, start_date=None, end_date=None):
        """Get expenses grouped by category"""
        query = self.session.query(
            Category.name,
            Category.icon,
            Category.color,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).join(Expense).filter(Expense.user_id == self.user_id)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        query = query.group_by(Category.id).order_by(func.sum(Expense.amount).desc())
        
        results = query.all()
        
        total_expenses = sum(r.total for r in results)
        
        return [{
            'name': r.name,
            'icon': r.icon,
            'color': r.color,
            'total': round(r.total, 2),
            'count': r.count,
            'percentage': round((r.total / total_expenses * 100) if total_expenses > 0 else 0, 1)
        } for r in results]
    
    def get_monthly_trends(self, months=6):
        """Get monthly spending trends for the last N months"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=months * 30)
        
        query = self.session.query(
            extract('year', Expense.date).label('year'),
            extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == self.user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by('year', 'month').order_by('year', 'month')
        
        results = query.all()
        
        return [{
            'month': f"{int(r.year)}-{int(r.month):02d}",
            'total': round(r.total, 2)
        } for r in results]
    
    def get_weekly_trends(self, weeks=4):
        """Get weekly spending trends"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(weeks=weeks)
        
        expenses = self.session.query(Expense).filter(
            Expense.user_id == self.user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).all()
        
        # Group by week
        weekly_data = defaultdict(float)
        for expense in expenses:
            week_start = expense.date - timedelta(days=expense.date.weekday())
            week_key = week_start.strftime('%Y-%m-%d')
            weekly_data[week_key] += expense.amount
        
        return [{'week': k, 'total': round(v, 2)} for k, v in sorted(weekly_data.items())]
    
    def get_daily_trends(self, days=30):
        """Get daily spending trends"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        query = self.session.query(
            Expense.date,
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == self.user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by(Expense.date).order_by(Expense.date)
        
        results = query.all()
        
        return [{
            'date': r.date.strftime('%Y-%m-%d'),
            'total': round(r.total, 2)
        } for r in results]
    
    def get_salary_comparison(self, month=None, year=None):
        """Compare monthly expenses with salary"""
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        user = self.session.query(User).filter_by(id=self.user_id).first()
        
        total_expenses = self.session.query(
            func.sum(Expense.amount)
        ).filter(
            Expense.user_id == self.user_id,
            extract('month', Expense.date) == month,
            extract('year', Expense.date) == year
        ).scalar() or 0
        
        salary = user.salary if user else 0
        savings = salary - total_expenses
        savings_percentage = (savings / salary * 100) if salary > 0 else 0
        
        return {
            'salary': round(salary, 2),
            'expenses': round(total_expenses, 2),
            'savings': round(savings, 2),
            'savings_percentage': round(savings_percentage, 1),
            'overspending': total_expenses > salary
        }
    
    def get_top_spending_categories(self, limit=5, start_date=None, end_date=None):
        """Get top N spending categories"""
        all_categories = self.get_category_wise_expenses(start_date, end_date)
        return all_categories[:limit]
    
    def get_highest_spending_day(self, month=None, year=None):
        """Get the day with highest spending in a month"""
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        query = self.session.query(
            Expense.date,
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == self.user_id,
            extract('month', Expense.date) == month,
            extract('year', Expense.date) == year
        ).group_by(Expense.date).order_by(func.sum(Expense.amount).desc())
        
        result = query.first()
        
        if result:
            return {
                'date': result.date.strftime('%Y-%m-%d'),
                'day': result.date.strftime('%A'),
                'total': round(result.total, 2)
            }
        return None
    
    def get_household_expenses(self, start_date=None, end_date=None):
        """Get essential household expenses"""
        from config import Config
        
        query = self.session.query(
            Category.name,
            Category.icon,
            func.sum(Expense.amount).label('total')
        ).join(Expense).filter(
            Expense.user_id == self.user_id,
            Category.name.in_(Config.ESSENTIAL_BILLS)
        )
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        query = query.group_by(Category.id)
        
        results = query.all()
        
        return [{
            'name': r.name,
            'icon': r.icon,
            'total': round(r.total, 2)
        } for r in results]
    
    def check_budget_alerts(self, month=None, year=None):
        """Check for budget overspending alerts"""
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        budgets = self.session.query(Budget).filter_by(
            user_id=self.user_id,
            alerts_enabled=True
        ).all()
        
        alerts = []
        
        for budget in budgets:
            spent = self.session.query(
                func.sum(Expense.amount)
            ).filter(
                Expense.user_id == self.user_id,
                Expense.category_id == budget.category_id,
                extract('month', Expense.date) == month,
                extract('year', Expense.date) == year
            ).scalar() or 0
            
            percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
            
            if percentage >= 90:
                category = self.session.query(Category).filter_by(id=budget.category_id).first()
                alerts.append({
                    'category': category.name if category else 'Unknown',
                    'spent': round(spent, 2),
                    'budget': round(budget.monthly_limit, 2),
                    'percentage': round(percentage, 1),
                    'exceeded': spent > budget.monthly_limit
                })
        
        return alerts
    
    def forecast_expenses(self, months_ahead=1):
        """Simple expense forecasting using moving average"""
        # Get last 3 months of data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)
        
        monthly_totals = []
        for i in range(3):
            month_start = end_date - timedelta(days=(i+1)*30)
            month_end = end_date - timedelta(days=i*30)
            
            total = self.session.query(
                func.sum(Expense.amount)
            ).filter(
                Expense.user_id == self.user_id,
                Expense.date >= month_start,
                Expense.date <= month_end
            ).scalar() or 0
            
            monthly_totals.append(total)
        
        # Simple moving average
        if monthly_totals:
            forecast = sum(monthly_totals) / len(monthly_totals)
            return round(forecast, 2)
        
        return 0
    
    def get_all_users_expenses(self):
        """Get expenses for all users (household total)"""
        query = self.session.query(
            User.username,
            func.sum(Expense.amount).label('total')
        ).join(Expense).group_by(User.id).order_by(func.sum(Expense.amount).desc())
        
        results = query.all()
        
        return [{
            'username': r.username,
            'total': round(r.total, 2)
        } for r in results]
    
    def close(self):
        """Close database session"""
        self.session.close()
