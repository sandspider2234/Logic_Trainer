import random
from BinTree import BinTree
import flask
import flask_login
import forms
import db

app = flask.Flask(__name__)
app.config.from_object('config')
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(flask_login.UserMixin):
    def __init__(self, username, primary_id, difficulty, active=True):
        self.username = username
        self.primary_id = primary_id
        self.difficulty = difficulty
        self.active = active

    def get_id(self):
        return str(self.primary_id).encode().decode()

    def is_active(self):
        return self.active


@login_manager.user_loader
def load_user(user_id):
    try:
        with db.create_connection() as connection, connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id=%s"
            cursor.execute(sql, (user_id))
            result = cursor.fetchone()
        if result:
            return User(result['username'], result['id'], result['difficulty'])
        return None
    except:
        return None


def generate_statement_string(sections, rand_min=-100, rand_max=100):
    statement_str = ''
    while sections > 0:
        statement_str += ' '.join([random.choice(['x', 'y', str(random.randint(rand_min, rand_max))]),
                                   random.choice(['>', '<', '==', '!=', '>=', '<=']),
                                   random.choice(['x', 'y', str(random.randint(rand_min, rand_max))])])
        if sections == 1:
            return statement_str
        statement_str += ' ' + random.choice(['||', '&&']) + ' '
        sections -= 1


@app.route('/', methods=['GET', 'POST'])
def home():
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    if flask_login.current_user.is_anonymous:
        statement_str = generate_statement_string(2)
    else:
        statement_str = generate_statement_string(flask_login.current_user.difficulty)
    tree = BinTree.build_tree(statement_str)
    statement_result = BinTree.solve_tree(tree, x, y)
    form = forms.TrueOrFalseForm(flask.request.form)
    if form.validate_on_submit():
        if not flask_login.current_user.is_anonymous:
            difficulty = flask_login.current_user.difficulty
            if form.choice.data == form.hidden.data:
                with db.create_connection() as connection, connection.cursor() as cursor:
                    sql = "UPDATE users SET score = score + %s WHERE id = %s"
                    cursor.execute(sql, (difficulty, flask_login.current_user.primary_id))
                    connection.commit()
                    flask.flash('Correct! +{0} points!'.format(difficulty), 'success')
            else:
                with db.create_connection() as connection, connection.cursor() as cursor:
                    sql = "UPDATE users SET score = score - %s WHERE id = %s"
                    cursor.execute(sql, (difficulty / 2, flask_login.current_user.primary_id))
                    connection.commit()
                    flask.flash('Incorrect! -{0} points!'.format(difficulty / 2), 'error')
        else:
            if form.choice.data == form.hidden.data:
                flask.flash('Correct!', 'success')
            else:
                flask.flash('Incorrect!', 'error')
    elif form.errors:
        for item in form.errors.items():
            flask.flash(item, 'error')
    return flask.render_template('home.html', x_value=str(x), y_value=str(y), statement=statement_str,
                                 result=str(statement_result), form=form)


@app.route('/tester', methods=['GET', 'POST'])
def tester():
    form = forms.StatementForm()
    if form.validate_on_submit():
        try:
            solution = BinTree.solve_tree(BinTree.build_tree(form.statement.data))
            if type(solution) is not bool:
                raise ValueError
            flask.flash('Given statement is {0}, solution is {1}'.format(form.statement.data, str(solution)))
        except (ValueError, IndexError):
            flask.flash('Invalid statement!', 'error')
    elif form.errors:
        for item in form.errors.items():
            flask.flash(item, 'error')
    return flask.render_template('tester.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not flask_login.current_user.is_anonymous:
        flask.flash('Already logged in!', 'error')
        return flask.redirect('/')
    login_form = forms.LoginForm(prefix='login_form')
    signup_form = forms.SignupForm(prefix='signup_form')
    if signup_form.register.data and signup_form.validate_on_submit():
        with db.create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username=%s OR email=%s"
                cursor.execute(sql, (signup_form.username.data, signup_form.email.data))
                result = cursor.fetchone()
                if result:
                    flask.flash('Username or email already exist!', 'error')
                    return flask.redirect('/login')
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, SHA1(%s))"
                cursor.execute(sql, (signup_form.username.data, signup_form.email.data, signup_form.password.data))
                connection.commit()
        with db.create_connection() as connection, connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s AND password=SHA1(%s)"
            cursor.execute(sql, (signup_form.username.data, signup_form.password.data))
            result = cursor.fetchone()
            if flask_login.login_user(load_user(result['id'])):
                flask.flash('User created and logged in!', 'success')
                return flask.redirect('/')
            else:
                flask.flash('User created but not logged in.')
    elif signup_form.errors:
        for item in signup_form.errors.items():
            flask.flash(item, 'error')

    if login_form.login.data and login_form.validate_on_submit():
        with db.create_connection() as connection, connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s AND password=SHA1(%s)"
            cursor.execute(sql, (login_form.username.data, login_form.password.data))
            result = cursor.fetchone()
            if result:
                if flask_login.login_user(load_user(result['id']), remember=login_form.remember_me.data):
                    flask.flash('Logged in!', 'success')
                    return flask.redirect('/')
                else:
                    flask.flash('Sorry, something went wrong.', 'error')
            else:
                flask.flash('Invalid username or password.', 'error')
    elif login_form.errors:
        for item in login_form.errors.items():
            flask.flash(item, 'error')

    return flask.render_template('login.html', login_form=login_form, signup_form=signup_form)


@app.route('/about')
def about():
    return flask.render_template('about.html')


@app.route('/user/<name>')
def profile(name):
    with db.create_connection() as connection, connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username=%s"
        cursor.execute(sql, (name))
        result = cursor.fetchone()
    if not result:
        flask.flash('No such user!')
        return flask.redirect('/')
    return flask.render_template('profile.html', score=result['score'], username=name)


@app.route('/leaderboard')
def leaderboard():
    with db.create_connection() as connection, connection.cursor() as cursor:
        sql = "SELECT * FROM users ORDER BY score DESC"
        cursor.execute(sql)
        user_dict = cursor.fetchall()
    return flask.render_template('leaderboard.html', user_dict=user_dict)


@app.route('/dashboard', methods=['GET', 'POST'])
@flask_login.login_required
def dashboard():
    form = forms.DifficultyForm()
    if form.validate_on_submit():
        with db.create_connection() as connection, connection.cursor() as cursor:
            sql = "UPDATE users SET difficulty = %s WHERE id = %s"
            cursor.execute(sql, (form.difficulty.data, flask_login.current_user.primary_id))
            connection.commit()
            flask.flash("Difficulty updated! Good luck!", 'success')
            return flask.redirect('/')
    elif form.errors:
        flask.flash(form.errors, 'error')
    return flask.render_template('dashboard.html', form=form)


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flask.flash('Logged out.')
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
