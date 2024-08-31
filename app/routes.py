from flask import Blueprint, render_template, request
import pandas as pd
import os

main = Blueprint('main', __name__)

DATA_DIR = os.path.join(os.getcwd(), 'data')
EXCEL_FILE = os.path.join(DATA_DIR, "bike_data.xlsx")

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/petrol', methods=['GET', 'POST'])
def petrol():
    if request.method == 'POST':
        petrol_price = request.form['petrol_price']
        liters = request.form['liters']
        kilometers = request.form['kilometers']

        new_data = pd.DataFrame({
            'Petrol Price': [petrol_price],
            'Liters': [liters],
            'Kilometers': [kilometers]
        })

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        if not os.path.exists(EXCEL_FILE):
            new_data.to_excel(EXCEL_FILE, index=False)
        else:
            existing_data = pd.read_excel(EXCEL_FILE)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            updated_data.to_excel(EXCEL_FILE, index=False)

        return "Data added successfully"
    return render_template('petrol.html')

@main.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        service_date = request.form['service_date']
        amount_paid = request.form['amount_paid']
        mileage = request.form['mileage']
        oil_changed = request.form.get('oil_changed', 'No')

        # Your logic to save the service data goes here
        # For now, we'll just return a success message
        return f"Service data saved: Date={service_date}, Amount={amount_paid}, Mileage={mileage}, Oil Changed={oil_changed}"
    return render_template('service.html')
