from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

DB_NAME = "studycase2.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studycase2.db"
app.config["SECRET_KEY"] = "dbjbjbjl"
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)







@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST" :
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")


        search = Users.query.filter_by(email=email).first()

        if search != None :
            flash("This e-mail already registered. Click 'Login' on the homepage")
            return render_template("register.html")


        new_user = Users(name=name, surname=surname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        search = Users.query.filter_by(email=email).first()

        if search is None:
            flash("User not found")
            return render_template("login.html")

        if password == search.password:
            return render_template("userspage.html")
        else:
            flash("Wrong password")
            return render_template("login.html")

    return render_template("login.html")


@app.errorhandler(404)
def error(e):
    return render_template("404.html")


if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

#tasarım için bootstra'ten css ve js ekledim bazı html lere
#flash html ini buradan: https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/  kopyala yapıştır