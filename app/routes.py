from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash
import datetime
import pandas as pd
import os

main = Blueprint('main', __name__)

bike_data='data/bike_data.csv'
service_data='data/service_data.csv'

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
        #1sttime
        # columns = ['Datetime', 'Kilometers', 'Petrol Price', 'Liters']
        # empty_df = pd.DataFrame(columns=columns)
        # empty_df.to_csv(bike_data, index=False)

        existing_data = pd.read_csv(bike_data)
        existing_data.columns = ['Datetime', 'Kilometers', 'Petrol Price', 'Liters']
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(bike_data, index=False)
                
        flash('Petrol data added successfully!')
        return redirect(url_for('main.petrol'))
    
    return render_template('petrol.html')

@main.route('/view_petrol')
def view_petrol():
    data = pd.read_csv(bike_data)

    # Rename columns to match those in HTML template
    data.columns = ['Datetime', 'Kilometers', 'Petrol Price', 'Liters']

    # Convert the DataFrame to a list of dictionaries
    records = data.to_dict(orient='records')
    
    return render_template('view_petrol.html', data=records)

@main.route('/delete_petrol/<int:index>', methods=['GET'])
def delete_petrol(index):
    # Load existing petrol data
    if os.path.exists(bike_data):
        data = pd.read_csv(bike_data)
        
        # Drop the record at the specified index
        data = data.drop(index)
        
        # Save the updated DataFrame back to the Excel file
        data.to_csv(bike_data, index=False)
    
    # Redirect to the view_petrol page after deletion
    return redirect(url_for('main.view_petrol'))

@main.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        # Handle form submission for service data
        service_date =datetime.datetime.now()
        mileage = request.form['mileage']
        amount_paid = request.form['amount']
        oil_changed = request.form['oil_changed']
        new_data = pd.DataFrame({
            'Service Date': [service_date],
            'Mileage': [mileage],
            'Amount Paid': [amount_paid],
            'Oil Changed': [oil_changed]
        })
        existing_data = pd.read_csv(service_data)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(service_data, index=False)
        return redirect(url_for('main.view_service'))
    return render_template('service.html')

@main.route('/view_service')
def view_service():
    # Load service data and render view_service.html
    data = pd.read_csv(service_data)

    # Rename columns to match those in HTML template
    data.columns = ['Service Date', 'Mileage', 'Amount Paid', 'Oil Changed']

    # Convert the DataFrame to a list of dictionaries
    records = data.to_dict(orient='records')
    
    return render_template('view_service.html', data=records)




@main.route('/delete_service/<int:index>', methods=['GET'])
def delete_service(index):
    # Load existing petrol data
    if os.path.exists(service_data):
        data = pd.read_csv(service_data)
        
        # Drop the record at the specified index
        data = data.drop(index)
        
        # Save the updated DataFrame back to the Excel file
        data.to_csv(service_data, index=False)
    
    # Redirect to the view_service page after deletion
    return redirect(url_for('main.view_service'))
