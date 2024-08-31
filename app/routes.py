from flask import Blueprint, render_template, request
import pandas as pd
import os

main = Blueprint('main', __name__)

# Define the directory and Excel file path
DATA_DIR = os.path.join(os.getcwd(), 'data')
EXCEL_FILE = os.path.join(DATA_DIR, "bike_data.xlsx")

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/add_data', methods=['POST'])
def add_data():
    # Example data: petrol_price, liters, kilometers
    petrol_price = request.form['petrol_price']
    liters = request.form['liters']
    kilometers = request.form['kilometers']

    # Create a DataFrame with the new data
    new_data = pd.DataFrame({
        'Petrol Price': [petrol_price],
        'Liters': [liters],
        'Kilometers': [kilometers]
    })

    # Ensure the data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Check if the Excel file exists
    if not os.path.exists(EXCEL_FILE):
        # If the file doesn't exist, create it and write the new data
        new_data.to_excel(EXCEL_FILE, index=False)
    else:
        # If the file exists, read the existing data, append the new data, and save it
        existing_data = pd.read_excel(EXCEL_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_excel(EXCEL_FILE, index=False)

    return "Data added successfully"
