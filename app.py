import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create Models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    print(request.args.get('q'))
    # if
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    completed_todo = Todo.query.filter_by(complete=True).count()
    # uncompleted_todo = Todo.query.filter_by(complete=False).count()
    uncompleted_todo = total_todo - completed_todo # both logics or correct which one is ur wish to use
    # return render_template('dashboard/index.html',todo_list=todo_list, total_todo=total_todo, completed_todo=completed_todo,uncompleted_todo=uncompleted_todo)
    return render_template('dashboard/index.html',**locals())  # Either use local variables locals() or variable=variable

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('dashboard/about.html')

@app.route('/search')
def search(title):    
    q = request.args.get("q")

    if q:
        todo = Todo.query.filter(Todo.title.contains(q) |
        Todo.id.contains(q))
    else:
        todo = Todo.query.all()
    return render_template('dashboard/search.html',q=q)

    # # q="%{}%".format(q)
    # # todo = Todo.query.filter(todo.title.like(q)).all()
    # return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)