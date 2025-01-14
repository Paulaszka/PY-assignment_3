from flask import Flask, request, render_template, redirect, jsonify
import os
import database

app = Flask(__name__)

# Configure connection to PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/postgres'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)


# Data model
class Numbers(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key=True)
    number1 = database.db.Column(database.db.Float, nullable=False)
    number2 = database.db.Column(database.db.Float, nullable=False)
    category = database.db.Column(database.db.Integer, nullable=False)


# Display data
@app.route('/', methods=['GET'])
def index():
    numbers = Numbers.query.all()
    return render_template('index.html', numbers=numbers)


# Add data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        number1 = request.form.get('number1')
        number2 = request.form.get('number2')
        category = request.form.get('category')

        # Check if all parameters are present
        if not all([number1, number2, category]):
            return render_template('error400.html', message="Error 400: All fields are required"), 400

        # Data validation
        try:
            number1 = float(number1)
            number2 = float(number2)
            category = int(category)
        except ValueError:
            return render_template('error400.html', message="Error 400: Invalid data type"), 400

        if float(category) != int(float(category)):
            return render_template('error400.html', message="Error 400: Category must be an integer, not a float"), 400

        new_record = Numbers(number1=number1, number2=number2, category=category)
        database.add_row(new_record)
        return redirect('/')
    return render_template('add.html')


# Delete data
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    record_to_delete = Numbers.query.get(id)

    # Check if id was found in database
    if record_to_delete is None:
        return render_template('error404.html', message="Error 404: Record not found"), 404

    database.delete_row(record_to_delete)
    return redirect('/')


# Display data points
@app.route('/api/data', methods=['GET'])
def get_data():
    numbers = Numbers.query.all()
    data = []
    for number in numbers:
        data.append({
            'id': number.id,
            'number1': number.number1,
            'number2': number.number2,
            'category': number.category
        })
    return jsonify(data)


# Add a new data point
@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.get_json()

    # Check if all required fields are present
    for field in ['number1', 'number2', 'category']:
        if field not in data:
            return jsonify({'error': 'Missing required field: ' + field}), 400

    # Data validation
    if isinstance(data['category'], float):
        return jsonify({'error': 'category must be an integer, not a float'}), 400

    try:
        number1 = float(data['number1'])
        number2 = float(data['number2'])
        category = int(data['category'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data type'}), 400

    new_record = Numbers(number1=number1, number2=number2, category=category)
    database.add_row(new_record)

    return jsonify({'id': new_record.id}), 201


# Delete a data point by id
@app.route('/api/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    record_to_delete = Numbers.query.get(id)

    if record_to_delete is None:
        return jsonify({'error': 'Record not found'}), 404

    database.delete_row(record_to_delete)
    return jsonify({'id': id}), 200


if __name__ == '__main__':
    app.run()
