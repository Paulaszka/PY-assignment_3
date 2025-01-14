from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def add_row(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def get_row(obj_class, obj_id):
    return db.session.get(obj_class, obj_id)


def delete_row(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
