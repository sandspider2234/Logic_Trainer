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


class User(flask_login.UserMixin):
    def __init__(self, username, primary_id, active=True):
        self.username = username
        self.primary_id = primary_id
        self.active = active

    def get_id(self):
        return str(self.primary_id).encode().decode()

    def is_active(self):
        return self.active


@login_manager.user_loader
def load_user(user_id):
    try:
        with db.create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE id=%s"
                cursor.execute(sql, (user_id))
                result = cursor.fetchone()
        if result:
            return User(result['username'], result['id'])
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
    statement_str = generate_statement_string(2)
    tree = BinTree.build_tree(statement_str)
    statement_result = BinTree.solve_tree(tree, x, y)
    form = forms.TrueOrFalseForm(flask.request.form)
    if form.validate_on_submit():
        if not flask_login.current_user.is_anonymous:
            if form.choice.data == form.hidden.data:
                with db.create_connection() as connection, connection.cursor() as cursor:
                    sql = "UPDATE users SET score = score + 2 WHERE id = %s"
                    cursor.execute(sql, flask_login.current_user.get_id())
                    connection.commit()
                    flask.flash('Correct! +2 points!')
            else:
                with db.create_connection() as connection, connection.cursor() as cursor:
                    sql = "UPDATE users SET score = score - 1 WHERE id = %s"
                    cursor.execute(sql, flask_login.current_user.primary_id)
                    connection.commit()
                    flask.flash('Incorrect! -1 points!')
        else:
            if form.choice.data == form.hidden.data:
                flask.flash('Correct!')
            else:
                flask.flash('Incorrect!')
    return flask.render_template('home.html', x_value=str(x), y_value=str(y), statement=statement_str,
                                 result=str(statement_result), form=form)


@app.route('/tester', methods=['GET', 'POST'])
def tester():
    form = forms.StatementForm()
    if form.validate_on_submit():
        try:
            solution = BinTree.solve_tree(BinTree.build_tree(form.statement.data), 0, 0)
            if type(solution) is not bool:
                raise ValueError
            flask.flash('Given statement is {0}, solution is {1}'.format(form.statement.data, str(solution)))
        except (ValueError, IndexError):
            flask.flash('Invalid statement!')
    return flask.render_template('tester.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not flask_login.current_user.is_anonymous:
        return flask.redirect('/')
    login_form = forms.LoginForm(prefix='login_form')
    signup_form = forms.SignupForm(prefix='signup_form')
    if signup_form.register.data and signup_form.validate_on_submit():
        with db.create_connection() as connection, connection.cursor() as cursor:
            sql = "INSERT INTO users (username, email, password, score) VALUES (%s, %s, SHA1(%s), 0);"
            cursor.execute(sql, (signup_form.username.data, signup_form.email.data, signup_form.password.data))
            connection.commit()
        flask.flash('Signed up! Please log in.')

    if login_form.login.data and login_form.validate_on_submit():
        with db.create_connection() as connection, connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s AND password=SHA1(%s)"
            cursor.execute(sql, (login_form.username.data, login_form.password.data))
            result = cursor.fetchone()
            if result:
                if flask_login.login_user(load_user(result['id']), remember=login_form.remember_me.data):
                    flask.flash('Logged in!')
                    return flask.redirect('/')
                else:
                    flask.flash('Sorry, something went wrong.')
            else:
                flask.flash('Invalid username or password.')

    return flask.render_template('login.html', login_form=login_form, signup_form=signup_form)


@app.route('/about')
def about():
    return flask.render_template('about.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
