import random
from BinTree.BinTree import build_tree, solve_tree
from flask import Flask, render_template
app = Flask(__name__)


def generate_statement_string():
    first_argument = random.choice(['x', 'y'])
    operator = random.choice(['>', '<', '==', '!=', '>=', '<='])
    second_argument = random.randint(-100, 100)
    statement_str = ''.join([first_argument, ' ', operator, ' ', str(second_argument)])
    return statement_str


@app.route('/')
def home():
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    statement_str = generate_statement_string()
    tree = build_tree(statement_str)
    statement_result = solve_tree(tree, x, y)
    return render_template('home.html', x_value=str(x), y_value=str(y), statement=statement_str, result=str(statement_result))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
