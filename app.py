from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfiguracja połączenia z bazą danych PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)


# Model danych
class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number1 = db.Column(db.Integer, nullable=False)
    number2 = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)


# Strona główna
@app.route('/', methods=['GET'])
def index():
    numbers = Numbers.query.all()
    return render_template('index.html', numbers=numbers)


# Wypisanie danych w tabeli
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        number1 = request.form['number1']
        number2 = request.form['number2']
        category = request.form['category']
        new_entry = Numbers(number1=number1, number2=number2, category=category)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


# Usuwanie danych
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    record_to_delete = Numbers.query.get_or_404(id)  # Pobierz rekord lub 404, jeśli nie istnieje
    db.session.delete(record_to_delete)
    db.session.commit()
    return redirect('/')  # Po usunięciu przekieruj do strony głównej


if __name__ == '__main__':
    # Tworzenie tabel w bazie danych, jeśli nie istnieją
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5050)
