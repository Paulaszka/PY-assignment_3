from flask_sqlalchemy import SQLAlchemy

# Init SQLAlchemy
db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    # Tworzenie tabel w bazie danych, jeśli jeszcze nie istnieją
    with app.app_context():
        db.create_all()


def add_row(obj):
    db.session.add(obj)
    db.session.commit()


def get_row(obj_class, obj_id):
    return db.session.get(obj_class, obj_id)


def delete_row(obj):
    db.session.delete(obj)
    db.session.commit()
