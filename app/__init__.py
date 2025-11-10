import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Створюємо об'єкти
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Секретний ключ для безпеки (потрібен для сесій та форм)
    app.config['SECRET_KEY'] = 'a_very_secret_key_123'

    # Налаштування бази даних
    # Локально ми будемо використовувати SQLite
    # На Heroku ми використаємо DATABASE_URL (з PostgreSQL)
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ініціалізуємо додатки
    db.init_app(app)
    login_manager.init_app(app)

    # Налаштування Flask-Login
    login_manager.login_view = 'main.login'  # Назва функції для сторінки логіну
    login_manager.login_message = 'Будь ласка, увійдіть.'

    # Імпортуємо моделі *після* створення db
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Реєструємо наші сторінки (routes)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Створюємо таблиці в БД (якщо їх немає)
    with app.app_context():
        db.create_all()

    return app