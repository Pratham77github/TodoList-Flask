from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#Runtime error solution - outside context
app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)
    desc = db.Column(db.String(300) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/' , methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title , desc = desc)
        db.session.add(todo)
        db.session.commit()

    altodo = Todo.query.all()
    return render_template('index.html',altodo = altodo)

@app.route('/update/<int:sno>' , methods = ['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html',todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    deltodo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(deltodo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)