import flask_login
import re
from flask import *
from FDataBase import FDataBase
import logging
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
#configuration (все перемнные заклавными буквами - конфигурационная инфа)
DATABASE = '/temp/flsite.db'
DEBUG = True
LOGSPAGE = 'Hm i think it is important /jkabcniunxkjnwjwklhu'
SECRET_KEY = '849_dljdslFJKmk$@GD$vVHr252'
PORT = 80

app = Flask(__name__)
app.config.from_object(__name__) #upload configuration in our application

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db'))) # переопределяем путь к бд

log_file = os.environ.get('FLASK_LOG_FILE', './logs/log1.txt')
app.config['LOG_FILE'] = log_file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def connect_db():
    conn=sqlite3.connect(app.config['DATABASE']) # connect to db
    conn.row_factory = sqlite3.Row               # предстовление записей не в виде кортежа а в виде словаря
    return conn


def create_db(): #function for creating db
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db(): #соединение с базой данных
    if not hasattr(g, 'link_db'): #проверка не существует ли у переменно g такое свойство
        g.link_db = connect_db()
    return g.link_db


def input_check(text):
    if re.search("^[A-Za-z0-9@.]+$",text):
        return True
    return False


def input_url_check(text):
    if re.search("^[A-Za-z0-9{}+*]+$",text):
        return True
    return False


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title="Страница не найдена")#можно добваить код 404 если написав его через запятую а так будпет код 200


@app.errorhandler(401)
def Unaftorized(error):
    return render_template('401.html', title="Ошибка авторизации")


@app.teardown_appcontext     #происходит когда происходит уничтожения контекста приложения
def close_db(error): # закрываем соединение с дб если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.before_request
def before_request(): # перед каждым запросом
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/profile/<username>")
def profile(username):
    if not input_url_check(username):
        return render_template_string("<h1>Malicious input detect!!!</h1>")
    else:
        if 'userLogged' not in session or session['userLogged'].partition('@')[0] != username:
            #abort(401)
            template = f"<h1> You are not a {username} </h1>"
            return render_template_string(template)
        flag = dbase.getUserByEmail(session['userLogged'])
        return render_template('profile.html', title='Home', user=username, flag=flag['status'])


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET','POST'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged'].partition('@')[0]))
    elif request.method == 'POST':
        if (input_check(request.form['email'])) and (input_check(request.form['password'])):
            user = dbase.getUserByEmail(request.form['email'])
            if user and check_password_hash(user['password'], request.form['password']):
                session['userLogged']=request.form['email']
                logger.info('user: '+request.form['email']+'; password: '+request.form['password'])
                return redirect(url_for('profile', username=session['userLogged'].partition('@')[0]))
        else:
            logger.warning('bad input by: ' + request.form['email'])
    return render_template('login.html', title='Login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('userLogged', None)
    return redirect(url_for('login'))


@app.route("/register", methods=['GET','POST'])
def registration():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged'].partition('@')[0]))
    if request.method == 'GET':
        return render_template('register.html', title='Registration')
    elif request.method == 'POST':
        if not input_check(request.form['email']) or not input_check(request.form['password']) or not input_check(request.form['Confirm password']):
            flash('Bad characters', category='error')
            logger.warning('bad input by: '+request.form['email'])
        else:
            if not dbase.getUserByEmail(request.form['email']):
                if request.form['password'] == request.form['Confirm password']:
                    if request.form['email'].find('@') == -1:
                        flash('Email does not exist @', category='error')
                    else:
                        password_hash = generate_password_hash(request.form['password']) #!!!!!!!!!!!!!!!!!!!!!!!!
                        if dbase.addPost(request.form['email'], password_hash):
                            return redirect(url_for('login'))
                else:
                    flash('Passwords are not equal', category='error')
            else:
                flash('User exists',category='error')
    return render_template('register.html', title='Registration')


@app.route('/jkabcniunxkjnwjwklhu')
def logs():
    with open(app.config['LOG_FILE'], 'r') as f:
        logs = f.read().splitlines()
    return render_template('logs.html', log=logs)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0' ,port=5000)
    