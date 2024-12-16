from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure connection to PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init SQLAlchemy
db = SQLAlchemy(app)


# Data model
class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number1 = db.Column(db.Float, nullable=False)
    number2 = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, nullable=False)


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

        # Validate data
        try:
            number1 = float(number1)
            number2 = float(number2)
        except ValueError:
            return render_template('error400.html', message="Error 400: Invalid features"), 400

        try:
            category = int(category)
        except ValueError:
            return render_template('error400.html', message="Error 400: Invalid category"), 400

        new_entry = Numbers(number1=number1, number2=number2, category=category)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


# Delete data
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    record_to_delete = Numbers.query.get(id)
    if record_to_delete is None:
        return render_template('error404.html', message="Error 404: Record not found"), 404

    db.session.delete(record_to_delete)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    # Creating tables in database if they do not exist
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5050)
