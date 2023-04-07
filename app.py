from flask import Flask, render_template

app = Flask(__name__)

data = [
    {'name': 'Alice', 'age': 25, 'email': 'alice@example.com'},
    {'name': 'Bob', 'age': 30, 'email': 'bob@example.com'},
    {'name': 'Charlie', 'age': 35, 'email': 'charlie@example.com'},
    {'name': 'Dave', 'age': 40, 'email': 'dave@example.com'},
]

@app.route('/')
def index():
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
