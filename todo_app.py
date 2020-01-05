from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    title = db.Column(db.String(40), nullable=False)
    note = db.Column(db.String(250))

    def __repr__(self):
        return f"ToDoList('{self.title}','{self.note}')"


db.create_all()


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
            return "ADD Error..."

    else:
        tasks = ToDoList.query.order_by(ToDoList.id).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task = ToDoList.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return "DELETE ERROR..."
    return ""


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = ToDoList.query.get_or_404(id)
    if request.method == "POST":
        task.title = request.form["title"]
        task.note = request.form["note"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "UPDATE ERROR..."
    else:
        return render_template("update.html", task=task)


@app.route("/done/<int:id>")
def done(id):
    task = ToDoList.query.get_or_404(id)
    task.done = not task.done
    try:
        db.session.commit()
        return redirect("/")
    except:
        return "DONE ERROR..."


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


# done
# category
# easter egg: https://youtu.be/nxUmibwHKcM js obfuscated script
