# Daily Expense Tracker 💰

A comprehensive web application for tracking personal and household expenses with advanced analytics, visualizations, and reporting capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Features

### 1. **Daily Expense Recording**
- Record daily spending across multiple categories (Food, Travel, Bills, Shopping, etc.)
- Each entry includes date, category, amount, and detailed notes
- Quick add expense form on dashboard for convenience

### 2. **Category-Wise Expense Analysis**
- Expenses grouped into customizable categories with icons and colors
- Identify top spending categories and patterns
- Visual breakdown with percentages

### 3. **Household Expense Tracking**
- Track essential household bills (Rent, Utilities, Groceries, etc.)
- Month-to-month comparison for optimization
- Dedicated household analytics dashboard

### 4. **Monthly & Weekly Spending Trends**
- Interactive charts showing spending patterns
- Daily, weekly, and monthly trend analysis
- Identify peak spending periods

### 5. **Salary vs Monthly Expense Comparison**
- Compare total monthly expenses with income
- Automatic savings calculation
- Financial health status indicator

### 6. **Savings & Overspending Analysis**
- Real-time savings tracking
- Budget alerts when limits are exceeded
- Category-wise budget management

### 7. **Expense Forecasting**
- Predict future expenses using historical data
- Simple moving average calculations
- Plan budgets for upcoming months

### 8. **Expense Distribution Dashboard**
- **Category-wise pie chart** - Visual distribution of expenses
- **Monthly bar charts** - Track spending trends over time
- **Weekly/daily line charts** - Detailed time-based analysis
- **Top 5 categories** - Identify major spending areas
- **Salary comparison** - Income vs expense visualization

### 9. **Export & Report Generation**
- Export data in CSV and Excel formats
- Date range and category filtering
- Pre-configured report templates (Monthly, Quarterly, Annual)
- Formatted Excel reports with styling

### 10. **Multi-User Support**
- Multiple family members can track expenses separately
- Combined household expense view
- Individual vs total spending comparison
- Per-user analytics and insights

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory:**
```bash
cd Daily-expense
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize the database:**
```bash
python init_db.py
```

This will create:
- Database tables
- Default expense categories
- Sample demo user with test data

4. **Run the application:**
```bash
python app.py
```

5. **Open your browser and visit:**
```
http://localhost:5000
```

## 📁 Project Structure

```
Daily-expense/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, Category, Expense, Budget)
├── analytics.py           # Analytics engine for calculations
├── exports.py             # Export functionality (CSV, Excel)
├── config.py              # Configuration settings
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Dashboard
│   ├── expenses.html     # Expense management
│   ├── analytics.html    # Analytics dashboard
│   ├── household.html    # Household tracking
│   ├── reports.html      # Export & reports
│   └── users.html        # Multi-user management
├── static/
│   ├── css/
│   │   └── style.css     # Premium modern styling
│   └── js/
│       └── app.js        # JavaScript utilities
└── expense_tracker.db    # SQLite database (created after init)
```

## 💡 Usage

### Adding Expenses
1. Use the "Quick Add Expense" form on the dashboard
2. Or navigate to the Expenses page for detailed entry
3. Select category, enter amount, date, and description

### Viewing Analytics
1. Navigate to the **Analytics** page
2. View interactive charts:
   - Category distribution
   - Monthly/weekly/daily trends
   - Top spending categories
   - Salary vs expense comparison

### Tracking Household Bills
1. Go to the **Household** page
2. View essential bills summary
3. Analyze month-to-month trends
4. Compare multi-user contributions

### Exporting Reports
1. Navigate to the **Reports** page
2. Select date range and category filters
3. Choose format (CSV or Excel)
4. Use quick templates for common reports

### Managing Multiple Users
1. Go to the **Users** page
2. View individual user statistics
3. Compare household contributions
4. Analyze combined savings

## 🎨 Features Highlights

### Premium Modern UI
- **Glassmorphism effects** for cards and modals
- **Vibrant color gradients** (avoiding generic colors)
- **Dark/Light mode** toggle with smooth transitions
- **Modern typography** using Google Fonts (Inter & Outfit)
- **Micro-animations** for enhanced user experience
- **Responsive design** for all screen sizes

### Advanced Analytics
- 6+ interactive Chart.js visualizations
- Real-time calculations
- Budget alerts and notifications
- Forecasting capabilities

### Data Management
- SQLite database for easy setup
- SQLAlchemy ORM for clean data access
- Pandas for advanced analytics
- Excel export with formatting

## 🛠️ Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js
- **Analytics:** Pandas
- **Export:** openpyxl for Excel generation
- **Styling:** Custom CSS with glassmorphism and gradients

## 📊 Default Categories

The application comes with 12 pre-configured categories:
- 🍔 Food
- 🚗 Travel
- 📄 Bills
- 🛍️ Shopping
- 🎬 Entertainment
- 🛒 Groceries
- ⚡ Utilities
- 🏥 Health
- 🏠 Household
- 📚 Education
- 🔑 Rent
- 📦 Other

## 🔐 Demo Credentials

After running `init_db.py`, you can use:
- **Username:** demo_user
- **Email:** demo@expense-tracker.com
- **Salary:** ₹50,000

The demo account includes 30 days of sample expenses for testing visualizations.

## 🎯 Future Enhancements

- User authentication and authorization
- Mobile app support
- Receipt scanning and OCR
- Recurring expense automation
- Budget recommendations using ML
- Cloud sync capabilities
- Multiple currency support

## 📝 License

MIT License - feel free to use and modify for your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For questions or support, please open an issue in the repository.

---

**Built with ❤️ for better financial management**
