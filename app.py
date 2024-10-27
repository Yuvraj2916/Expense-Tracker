from flask import Flask, render_template, request, redirect, session, url_for
import csv
import os

app = Flask(__name__)

BUDGET_FILE = "budget_data.csv"
BUDGET_AMOUNT_FILE = "budget_amount.txt"  
SAVINGS_FILE = "savings_data.csv"  
USERS_FILE = "users.csv"
savings_data = []

def initialize_files():
    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    if not os.path.exists(SAVINGS_FILE):
        with open(SAVINGS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Goal"])

def add_entry(date, category, amount, description):
    with open(BUDGET_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

def view_entries():
    entries = []
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            entries = list(reader)
    return entries

def total_spent():
    total = 0.0
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                total += float(row[2])
    return total

def save_budget_amount(amount):
    with open(BUDGET_AMOUNT_FILE, mode='w') as file:
        file.write(str(amount))

def load_budget_amount():
    if os.path.exists(BUDGET_AMOUNT_FILE):
        with open(BUDGET_AMOUNT_FILE, mode='r') as file:
            return float(file.read())
    return 0.0

def load_savings_data():
    savings = []
    if os.path.exists(SAVINGS_FILE):
        with open(SAVINGS_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            savings = list(reader)
    return savings

def save_savings_data(amount, goal):
    with open(SAVINGS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([amount, goal])

@app.route('/')
def home():
    entries = view_entries()
    total = total_spent()
    budget = load_budget_amount()
    remaining_budget = budget - total
    return render_template('index.html', entries=entries, total=total, budget=budget, remaining_budget=remaining_budget)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']
    add_entry(date, category, amount, description)
    return redirect('/')

@app.route('/savings', methods=['GET', 'POST'])
def savings():
    if request.method == 'POST':
        amount = request.form.get('amount')
        goal = request.form.get('goal')
        if amount and goal:
            save_savings_data(amount, goal)
            return redirect(url_for('savings'))
    
    savings_data = load_savings_data()
    return render_template('savings.html', savings=savings_data)

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        save_budget_amount(budget)
        return redirect('/')
    return render_template('set_budget.html')

@app.route('/about')
def about():
    team = [
        {"name": "Yuvraj", "role": "Backend Developer"},
        {"name": "Pavani", "role": "Backend Developer"},
        {"name": "Abhinav", "role": "Frontend Developer"},
        {"name": "Shreya", "role": "Frontend Developer"},
    ]
    return render_template('about.html', team=team)

if __name__ == "__main__":
    initialize_files()
    app.run(debug=True)
