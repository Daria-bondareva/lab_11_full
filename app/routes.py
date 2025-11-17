from flask import render_template, redirect, url_for, flash, request, Blueprint
from . import db
from .models import Album, User
from .forms import AlbumForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

# Створюємо "Blueprint" - набір маршрутів
main = Blueprint('main', __name__)


# --- Статичні сторінки ---

@main.route('/')
def index():
    albums = Album.query.all()
    return render_template('index.html', albums=albums)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/history')
def history():
    return render_template('history.html')


# --- Сторінка альбому (динамічна) ---

@main.route('/album/<int:album_id>')
def album(album_id):
    # .get_or_404() - зручно: або знайде, або покаже сторінку 404
    album = Album.query.get_or_404(album_id)
    return render_template('album.html', album=album)


# --- Вхід та Вихід (Автентифікація) ---

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Дуже спрощена перевірка пароля для лаби
        if user and user.password == form.password.data:
            login_user(user)
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неправильний логін або пароль.', 'danger')

    return render_template('login.html', form=form)


@main.route('/logout')
@login_required  # Доступ тільки для тих, хто увійшов
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# --- CRUD (Create, Read, Update, Delete) для Альбомів ---

@main.route('/add_album', methods=['GET', 'POST'])
@login_required
def add_album():
    form = AlbumForm()
    if form.validate_on_submit():
        new_album = Album(title=form.title.data,
                          release_year=form.release_year.data,
                          description=form.description.data,
                          cover_url=form.cover_url.data)
        db.session.add(new_album)
        db.session.commit()
        flash('Альбом успішно додано!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_album.html', form=form, title="Додати альбом")


@main.route('/edit_album/<int:album_id>', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    form = AlbumForm(obj=album)  # Заповнюємо форму даними з БД

    if form.validate_on_submit():
        album.title = form.title.data
        album.release_year = form.release_year.data
        album.description = form.description.data
        album.cover_url = form.cover_url.data
        db.session.commit()
        flash('Альбом оновлено!', 'success')
        return redirect(url_for('main.album', album_id=album.id))

    return render_template('edit_album.html', form=form, title="Редагувати альбом")


@main.route('/delete_album/<int:album_id>', methods=['POST'])  # Краще через POST
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    flash('Альбом видалено.', 'success')
    return redirect(url_for('main.index'))


@main.route('/reset-db-123')
def reset_db():
    db.drop_all()   # Видаляє все
    db.create_all() # Створює нову структуру з cover_url

    # Створюємо адміна знову
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', password='password123')
        db.session.add(user)
        db.session.commit()
    return "Базу оновлено! Можна додавати альбоми з картинками."