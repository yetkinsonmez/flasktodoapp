from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yetki/Desktop/ToDoApp/todo.db'
db = SQLAlchemy(app)
app.secret_key = "todo"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #oto artan bir int
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def main():
    todolist = Todo.query.all()
    return render_template("main.html",todolist=todolist)
    
@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)
    db.session.commit()
    flash("Your todo is added","success")
    return redirect(url_for("main"))

@app.route("/check/<string:id>")
def check(id):
    todo = Todo.query.filter_by(id=id).first()

    todo.complete = not todo.complete #false ise true; true ise false yap

    db.session.commit()
    return redirect(url_for("main"))

@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()

    db.session.delete(todo)

    db.session.commit()
    return redirect(url_for("main"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
