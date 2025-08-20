from flask import Flask,jsonify,request

app=Flask(__name__)

tasks=[]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_tasks():
    data=request.get_json()
    task={"id":len(tasks)+1,"Title":data["title"],"done":False}
    tasks.append(task)
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    for task in tasks:
        if tasks["id"]==task_id:
            tasks["done"]=True
            return jsonify(task)
        return jsonify({"error":"Task not found"}),404
    
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks=[task for task in tasks if tasks["id"]!=task_id]
    return jsonify({"message":"Task deleted."})

if __name__=="__main__":
    app.run(debug=True)
