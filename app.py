from flask import Flask,jsonify,request,render_template
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


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks=tasks.query.all()
    return jsonify([tasks.to_dict() for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_tasks():
    data=request.get_json()
    task=Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task=Task.query.get(task_id)
    if not task:
        return jsonify({"error":"Task not found"}),404
    task.done=True
    db.session.commit()
    return jsonify(task.to_dict())
    
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task=Task.query.get(task_id)
    if not task:
        return jsonify({"error":"Task not found"}),404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message":"Task deleted."})

if __name__=="__main__":
    app.run(debug=True)
