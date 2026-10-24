from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from datetime import datetime, timedelta
from models import get_session, User, Category, Expense, Budget
from analytics import ExpenseAnalytics
from exports import ExportManager
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

# Helper function to get current user (in a real app, this would use authentication)
def get_current_user_id():
    """Get current user ID - defaults to first user for demo"""
    session = get_session()
    user = session.query(User).first()
    session.close()
    return user.id if user else 1


@app.route('/')
def index():
    """Main dashboard"""
    user_id = get_current_user_id()
    session = get_session()
    
    # Get current month's data
    analytics = ExpenseAnalytics(user_id)
    
    # Get summary data
    today = datetime.now().date()
    first_day = today.replace(day=1)
    
    salary_comparison = analytics.get_salary_comparison()
    top_categories = analytics.get_top_spending_categories(limit=5)
    recent_expenses = session.query(Expense, Category).join(Category).filter(
        Expense.user_id == user_id
    ).order_by(Expense.date.desc()).limit(10).all()
    
    budget_alerts = analytics.check_budget_alerts()
    
    user = session.query(User).filter_by(id=user_id).first()
    
    analytics.close()
    session.close()
    
    return render_template('index.html',
                         user=user,
                         salary_comparison=salary_comparison,
                         top_categories=top_categories,
                         recent_expenses=recent_expenses,
                         budget_alerts=budget_alerts)


@app.route('/expenses')
def expenses():
    """Expense management page"""
    user_id = get_current_user_id()
    session = get_session()
    
    # Get filter parameters
    category_filter = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build query
    query = session.query(Expense, Category).join(Category).filter(Expense.user_id == user_id)
    
    if category_filter:
        query = query.filter(Category.name == category_filter)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    expenses_list = query.order_by(Expense.date.desc()).all()
    categories = session.query(Category).all()
    
    session.close()
    
    return render_template('expenses.html',
                         expenses=expenses_list,
                         categories=categories)


@app.route('/analytics')
def analytics_page():
    """Analytics dashboard"""
    user_id = get_current_user_id()
    analytics = ExpenseAnalytics(user_id)
    
    # Get various analytics
    category_wise = analytics.get_category_wise_expenses()
    monthly_trends = analytics.get_monthly_trends(months=6)
    weekly_trends = analytics.get_weekly_trends(weeks=8)
    daily_trends = analytics.get_daily_trends(days=30)
    salary_comparison = analytics.get_salary_comparison()
    top_categories = analytics.get_top_spending_categories(limit=5)
    highest_day = analytics.get_highest_spending_day()
    forecast = analytics.forecast_expenses()
    
    analytics.close()
    
    return render_template('analytics.html',
                         category_wise=json.dumps(category_wise),
                         monthly_trends=json.dumps(monthly_trends),
                         weekly_trends=json.dumps(weekly_trends),
                         daily_trends=json.dumps(daily_trends),
                         salary_comparison=salary_comparison,
                         top_categories=top_categories,
                         highest_day=highest_day,
                         forecast=forecast)


@app.route('/household')
def household():
    """Household expense tracking"""
    user_id = get_current_user_id()
    analytics = ExpenseAnalytics(user_id)
    
    # Get current month household expenses
    household_expenses = analytics.get_household_expenses()
    
    # Get month-to-month comparison for household items
    monthly_household = []
    for i in range(6):
        month_date = datetime.now() - timedelta(days=i*30)
        month_start = month_date.replace(day=1).date()
        
        if month_date.month == 12:
            month_end = month_date.replace(year=month_date.year + 1, month=1, day=1).date() - timedelta(days=1)
        else:
            month_end = month_date.replace(month=month_date.month + 1, day=1).date() - timedelta(days=1)
        
        expenses = analytics.get_household_expenses(month_start, month_end)
        total = sum(e['total'] for e in expenses)
        
        monthly_household.append({
            'month': month_date.strftime('%b %Y'),
            'total': round(total, 2),
            'items': expenses
        })
    
    monthly_household.reverse()
    
    # Get all users expenses
    all_users = analytics.get_all_users_expenses()
    
    analytics.close()
    
    return render_template('household.html',
                         household_expenses=household_expenses,
                         monthly_household=json.dumps(monthly_household),
                         all_users=all_users)


@app.route('/reports')
def reports():
    """Report generation page"""
    session = get_session()
    categories = session.query(Category).all()
    session.close()
    
    return render_template('reports.html', categories=categories)


@app.route('/users')
def users_page():
    """Multi-user management"""
    session = get_session()
    users = session.query(User).all()
    
    user_expenses = []
    for user in users:
        analytics = ExpenseAnalytics(user.id)
        comparison = analytics.get_salary_comparison()
        user_expenses.append({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'salary': user.salary
            },
            'expenses': comparison['expenses'],
            'savings': comparison['savings']
        })
        analytics.close()
    
    session.close()
    
    return render_template('users.html', user_expenses=user_expenses)


# API Endpoints

@app.route('/api/expenses', methods=['GET', 'POST', 'DELETE'])
def api_expenses():
    """API for expense operations"""
    user_id = get_current_user_id()
    session = get_session()
    
    if request.method == 'POST':
        # Add new expense
        data = request.json
        
        expense = Expense(
            user_id=user_id,
            category_id=data['category_id'],
            amount=float(data['amount']),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            description=data.get('description', ''),
            notes=data.get('notes', '')
        )
        
        session.add(expense)
        session.commit()
        
        session.close()
        return jsonify({'success': True, 'message': 'Expense added successfully'})
    
    elif request.method == 'DELETE':
        # Delete expense
        expense_id = request.args.get('id')
        expense = session.query(Expense).filter_by(id=expense_id, user_id=user_id).first()
        
        if expense:
            session.delete(expense)
            session.commit()
            session.close()
            return jsonify({'success': True, 'message': 'Expense deleted successfully'})
        
        session.close()
        return jsonify({'success': False, 'message': 'Expense not found'}), 404
    
    else:
        # Get expenses
        expenses = session.query(Expense, Category).join(Category).filter(
            Expense.user_id == user_id
        ).order_by(Expense.date.desc()).all()
        
        result = [{
            'id': exp.Expense.id,
            'category': exp.Category.name,
            'icon': exp.Category.icon,
            'amount': exp.Expense.amount,
            'date': exp.Expense.date.strftime('%Y-%m-%d'),
            'description': exp.Expense.description
        } for exp in expenses]
        
        session.close()
        return jsonify(result)


@app.route('/api/expense/<int:expense_id>', methods=['PUT'])
def api_update_expense(expense_id):
    """Update an expense"""
    user_id = get_current_user_id()
    session = get_session()
    
    expense = session.query(Expense).filter_by(id=expense_id, user_id=user_id).first()
    
    if not expense:
        session.close()
        return jsonify({'success': False, 'message': 'Expense not found'}), 404
    
    data = request.json
    
    if 'category_id' in data:
        expense.category_id = data['category_id']
    if 'amount' in data:
        expense.amount = float(data['amount'])
    if 'date' in data:
        expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'description' in data:
        expense.description = data['description']
    if 'notes' in data:
        expense.notes = data['notes']
    
    session.commit()
    session.close()
    
    return jsonify({'success': True, 'message': 'Expense updated successfully'})


@app.route('/api/export/csv')
def export_csv():
    """Export expenses to CSV"""
    user_id = get_current_user_id()
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category_id = request.args.get('category_id')
    
    exporter = ExportManager(user_id)
    csv_data = exporter.export_to_csv(start_date, end_date, category_id)
    exporter.close()
    
    from io import BytesIO
    output = BytesIO(csv_data.encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'expenses_{datetime.now().strftime("%Y%m%d")}.csv'
    )


@app.route('/api/export/excel')
def export_excel():
    """Export expenses to Excel"""
    user_id = get_current_user_id()
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category_id = request.args.get('category_id')
    
    exporter = ExportManager(user_id)
    excel_data = exporter.export_to_excel(start_date, end_date, category_id)
    exporter.close()
    
    return send_file(
        excel_data,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'expenses_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )


@app.route('/api/user/update_salary', methods=['POST'])
def update_salary():
    """Update user salary"""
    user_id = get_current_user_id()
    session = get_session()
    
    user = session.query(User).filter_by(id=user_id).first()
    
    if user:
        data = request.json
        user.salary = float(data['salary'])
        session.commit()
        session.close()
        return jsonify({'success': True, 'message': 'Salary updated successfully'})
    
    session.close()
    return jsonify({'success': False, 'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
