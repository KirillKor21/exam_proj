from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:secret@192.168.31.91:5432/bank_db"

db.init_app(app)


class Tbank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(64), nullable=False)
    full_sum = db.Column(db.Integer)
    overdraft_limit = db.Column(db.Integer)


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/view",  methods=['GET', 'POST'])
def view():
    return render_template("view.html")


@app.route("/fall")
def fall():
    return render_template("fall.html")


@app.route("/checking", methods=['POST'])
def cheking():
    username = request.form.get('username')
    token = request.form.get('token')
    if username and token and Tbank.query.filter_by(username=username).first():
        user = Tbank.query.filter_by(username=username).first()
        if user.token == token:

            return render_template("view.html", username=user.username, summ=user.full_sum, percent=percent(user.full_sum))
        else:
            return redirect("/fall")
    else:
        return redirect("/fall")


def percent(full_sum):
    if int(full_sum) > 1000000:
        perc = 9
    else:
        perc = 10 - int(full_sum) * 0.000001

    return perc


app.run(host="0.0.0.0")
