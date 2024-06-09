# import base64
import re
from flask import Flask, flash, request, jsonify, send_file
from flask_migrate import Migrate
# from app import app, db
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import io

UPLOAD_FOLDER = 'uploads'

#Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Configure MySQL connection
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sophie00?!@localhost/Shopokoa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

# # Configure the upload folder
# app.config['UPLOAD_FOLDER'] = 'uploads'
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

#iinitialze database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Define model for the database
class Customer(db.Model):
    # id = db.Column(db.Integer)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    national_Id = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    business_type = db.Column(db.String(120), nullable=False)
    business_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    licence_number = db.Column(db.String(20), primary_key=True)
    licence_image = db.Column(db.LargeBinary, nullable=False)  # Store the image data as a large binary object



    def repr(self):
        return f"<Customer {self.name}>"

# Routes fo creating new customer
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    national_Id = data['national_Id']
    email = data['email']
    phone_number = data['phoneNumber']
    business_type = data['business_type']
    business_name = data['business_name']
    location = data['location']
    licence_number = data['licence_number']
    
     # Handle file upload for licence file
    if 'licence_image' in request.files:
        licence_image = request.files['licence_image'].read()  # Read the file data
        filename = request.files['licence_image'].filename
    else:
        licence_image = None
        filename = None

     # Handle file upload for licence file (image or PDF)
    # Check if licence_image is provided
    licence_image = data.get('licence_image')
    if licence_image is None:
        return jsonify({'error': 'Licence image is required'}), 400

    

    # create a new customer
    new_customer = Customer(
        national_Id=national_Id, 
        email=email,first_name=first_name, 
        last_name=last_name, 
        phone_number=phone_number, 
        business_type=business_type, 
        business_name=business_name, 
        location=location, 
        licence_number=licence_number, 
        licence_image=licence_image
        )
    
    #add the new customer to the database
    db.session.add(new_customer)
    db.session.commit()

     # Check if the licence image was saved
    if licence_image:
        flash(f'Customer created successfully. Licence image saved as {filename}')
    else:
        flash('Customer created successfully, but no licence image was provided')
    return jsonify({'message': 'Customer created successfully'}), 201

# Define the new route to serve the licence image
@app.route('/get-image/<licence_number>', methods=['GET'])
def get_image(licence_number):
    # Query the database to get the customer by licence number
    customer = Customer.query.filter_by(licence_number=licence_number).first()

    # Check if the customer and the licence image exist
    if customer and customer.licence_image:
        # Serve the image file with the appropriate content type
        return send_file(io.BytesIO(customer.licence_image), mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Licence image not found'}), 404

# Serializer function
def serialize_form_data(first_name, last_name, phone_number, national_Id, email, location, license_number, licence_image_base64):
     # Combine first name, middle name, and last name to create full name
    full_name = f"{first_name} {last_name}".strip()

    return {
        'full_name': full_name,
        'National_Id': national_Id,
        'email': email,
        'phone_number': phone_number,
        'location': location,
        'license_number': license_number,
        # 'licence_image' :licence_image_base64
    }

@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Assuming the form data is sent as form
    form_data = request.form

    # print("Received form data:", form_data)
    # Extracting data from the form
    first_name = form_data.get('first_name')
    last_name = form_data.get('last_name')
    phoneNumber = form_data.get('phone_number')
    national_Id = form_data.get('national_Id')
    # full_name = form_data.get('full_name')
    email = form_data.get('email')
    location = form_data.get('location')
    license_number = form_data.get('licence_number')
    # licence_image = request.files['licence_image'].read()
    # Handle file uploaD
    if 'licence_image' in request.files:
        licence_image = request.files['licence_image']
        app.logger.info(f"Received file: {licence_image.filename}")
        # Save the file to the upload folder
        licence_image.save(os.path.join(app.config['UPLOAD_FOLDER'], licence_image.filename))
        app.logger.info(f"File saved to: {os.path.join(app.config['UPLOAD_FOLDER'], licence_image.filename)}")
    else:
        licence_image = None

    if licence_image:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], f'{license_number}.pdf'), 'wb') as f:
            f.write(licence_image.read())
            app.logger.info(f"File written to database with licence number: {license_number}")
    # Convert the binary image data to base64
    # licence_image_base64 = base64.b64encode(licence_image).decode('utf-8') if licence_image else None

    # Serializing form data
    serialized_data = serialize_form_data(first_name, last_name, phoneNumber, national_Id, email, location, license_number, licence_image)

    return jsonify(serialized_data)


# Validate ID function
def validate_id(idNo):
    # Example validation: ID should be numeric and have a length of 8
    if str(idNo).isdigit() and len(str(idNo)) == 8:
        return True
    else:
        return False

# Validate phone number function
def validate_phone_number(phoneNumber):
    # Example validation: Phone number should be numeric and have a length of 10 or 12
    if phoneNumber.isdigit() and len(phoneNumber) == 10 or len(phoneNumber) == 12:
        return True
    else:
        return False

# Convert phone number to international format
def convert_to_international(phoneNumber):
    if phoneNumber.startswith('0'):
        return '254' + phoneNumber[1:]
    else:
        return phoneNumber

# Validate email function
def validate_email(email):
    # Regular expression for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

# Route for validating ID, phone number, and email
@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    idNo = data.get('national_Id')
    phoneNumber = data.get('phone_number')
    email = data.get('email')

    if not validate_id(idNo):
        return jsonify({'error': 'Invalid ID!'}), 400

    # Convert phone number to international format
    phone_number_international = convert_to_international(phoneNumber)

    if not validate_phone_number(phone_number_international):
        return jsonify({'error': 'Invalid phone number!'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email!'}), 400

    return jsonify({'message': 'ID, phone number, and email are valid!'})

if __name__ == '__main__':
    app.run(debug=True)