import random
from BinTree import BinTree
import flask
import forms

app = flask.Flask(__name__)
app.config.from_object('config')


def generate_statement_string():
    first_argument = random.choice(['x', 'y'])
    first_operator = random.choice(['>', '<', '==', '!=', '>=', '<='])
    second_argument = random.choice([random.randint(-100, 100), 'x', 'y'])
    gate = random.choice(['||', '&&'])
    third_argument = random.choice(['x', 'y'])
    second_operator = random.choice(['>', '<', '==', '!=', '>=', '<='])
    fourth_argument = random.choice([random.randint(-100, 100), 'x', 'y'])
    statement_str = ''.join([first_argument, ' ', first_operator, ' ', str(second_argument), ' ', gate, ' ',
                             third_argument, ' ', second_operator, ' ', str(fourth_argument)])
    return statement_str


@app.route('/')
def home():
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    statement_str = generate_statement_string()
    tree = BinTree.build_tree(statement_str)
    statement_result = BinTree.solve_tree(tree, x, y)
    return flask.render_template('home.html', x_value=str(x), y_value=str(y), statement=statement_str, result=str(statement_result))


@app.route('/tester', methods=['GET', 'POST'])
def tester():
    form = forms.StatementForm()
    if form.validate_on_submit():
        try:
            if '\'";' in form.statement.data:
                raise ValueError
            solution = BinTree.solve_tree(BinTree.build_tree(form.statement.data), 0, 0)
            if type(solution) is not bool:
                raise ValueError
            flask.flash('Given statement is {0}, solution is {1}'.format(form.statement.data, str(solution)))
            flask.redirect('/tester')
        except (ValueError, IndexError):
            flask.flash('Invalid statement!')
            flask.redirect('/tester')
    return flask.render_template('tester.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm()
    signup_form = forms.SignupForm()
    return flask.render_template('login.html', login_form=login_form, signup_form=signup_form)


@app.route('/about')
def about():
    return flask.render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
