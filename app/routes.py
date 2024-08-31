from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash
import datetime
import pandas as pd
import os

main = Blueprint('main', __name__)

bike_data='data/bike_data.xlsx'
service_data='data/service_data.xlsx'

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/petrol', methods=['GET', 'POST'])
def petrol():
    if request.method == 'POST':
        date =datetime.datetime.now()
        mileage = request.form['mileage']
        petrol_price = request.form['petrol_price']  # Ensure this matches the name in the HTML form
        liters = request.form['liters']

        new_data = pd.DataFrame({
            'Datetime': [date],
            'Kilometers': [mileage],
            'Petrol Price': [petrol_price],
            'Liters': [liters]
        })

        existing_data = pd.read_excel(bike_data)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_excel(bike_data, index=False)
                
        flash('Petrol data added successfully!')
        return redirect(url_for('main.petrol'))
    
    return render_template('petrol.html')

@main.route('/view_petrol')
def view_petrol():
    data = pd.read_excel(bike_data)

    # Rename columns to match those in HTML template
    data.columns = ['Datetime', 'Kilometers', 'Petrol Price', 'Liters']

    # Convert the DataFrame to a list of dictionaries
    records = data.to_dict(orient='records')
    
    return render_template('view_petrol.html', data=records)

@main.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        # Handle form submission for service data
        service_date = request.form['service_date']
        mileage = request.form['mileage']
        amount_paid = request.form['amount_paid']
        oil_changed = request.form['oil_changed']
        new_data = pd.DataFrame({
            'Service Date': [service_date],
            'Mileage': [mileage],
            'Amount Paid': [amount_paid],
            'Oil Changed': [oil_changed]
        })
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(EXCEL_FILE):
            new_data.to_excel(EXCEL_FILE, index=False)
        else:
            existing_data = pd.read_excel(EXCEL_FILE)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            updated_data.to_excel(EXCEL_FILE, index=False)
        return redirect(url_for('main.view_service'))
    return render_template('service.html')

@main.route('/view_service')
def view_service():
    # Load service data and render view_service.html
    if os.path.exists(EXCEL_FILE):
        data = pd.read_excel(EXCEL_FILE)
    else:
        data = pd.DataFrame(columns=['Service Date', 'Mileage', 'Amount Paid', 'Oil Changed'])
    return render_template('view_service.html', data=data)


@main.route('/delete_petrol/<int:index>', methods=['GET'])
def delete_petrol(index):
    # Load existing petrol data
    if os.path.exists(bike_data):
        data = pd.read_excel(bike_data)
        
        # Drop the record at the specified index
        data = data.drop(index)
        
        # Save the updated DataFrame back to the Excel file
        data.to_excel(bike_data, index=False)
    
    # Redirect to the view_petrol page after deletion
    return redirect(url_for('main.view_petrol'))

