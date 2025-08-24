from flask import Flask,jsonify,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///tasks.db"
db=SQLAlchemy(app)

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    done=db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id":self.id,"title":self.title,"done":self.done }


with app.app_context():
    db.create_all()
    

@app.route("/")
def home():
    tasks=Task.query.all()
    return render_template("index.html",tasks=tasks)


@app.route("/tasks", methods=["POST"])
def add_tasks():
    title=request.form.get("title")
    if title:
        new_task=Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/tasks/<int:task_id>/done", methods=["POST"])
def mark_done(task_id):
    task=Task.query.get(task_id)
    if task:
        task.done=True
        db.session.commit()
    return redirect(url_for("home"))
    
@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    task=Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)