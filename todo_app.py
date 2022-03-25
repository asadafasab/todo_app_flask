from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class ToDoList(db.Model):
    """Main table of db"""
    task_id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    title = db.Column(db.String(40), nullable=False)
    note = db.Column(db.String(250))

    def __repr__(self):
        return f"ToDoList('{self.title}','{self.note}')"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        new_item = ToDoList(title=request.form["title"],
                            note=request.form["note"])

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect("/")
        except:
            return render_template("error.html", error="ADD")

    else:
        tasks = ToDoList.query.order_by(ToDoList.task_id).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = ToDoList.query.get_or_404(task_id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error.html", error="DELETE")
    return ""


@app.route("/update/<int:task_id>", methods=["POST", "GET"])
def update(task_id):
    task = ToDoList.query.get_or_404(task_id)
    if request.method == "POST":
        task.title = request.form["title"]
        task.note = request.form["note"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return render_template("error.html", error="UPDATE")
    else:
        return render_template("update.html", task=task)


@app.route("/done/<int:task_id>")
def done(task_id):
    task = ToDoList.query.get_or_404(task_id)
    task.done = not task.done
    try:
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error.html", error="DONE")


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="404 NOT FOUND"), 404


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="0.0.0.0")
