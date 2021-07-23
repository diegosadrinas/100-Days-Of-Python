from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, validators
import requests
from decouple import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config("SECRET_KEY")
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
moviedb_api_key = config("API_KEY")


class UpdateForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10", validators=[validators.DataRequired(), validators.NumberRange(min=0, max=10)])
    review = StringField(label="Your review", validators=[validators.DataRequired()])
    submit = SubmitField(label="Done")


class DeleteForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[validators.DataRequired()])
    submit = SubmitField(label="Add Movie")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=True)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String(250), unique=True, nullable=True)
    img_url = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return "Movie %r" % self.title


db.create_all()


@app.route("/")
def home():
    query = db.session.query(Movie)
    ordered_list = query.order_by(Movie.rating).all()
    if ordered_list:
        for movie in ordered_list:
            movie.ranking = len(ordered_list) - ordered_list.index(movie)
            db.session.commit()
    return render_template("index.html", movies=ordered_list)


@app.route("/edit", methods=["GET", "POST"])
def update():
    form = UpdateForm()
    movie_id = request.args.get("movie_id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(request.form["rating"])
        movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    movie_id = request.args.get("movie_id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = DeleteForm()
    titles_list = {}
    if form.validate_on_submit():
        params = {"api_key": moviedb_api_key,
                  "query": request.form["title"]}
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?", params=params)
        response.raise_for_status()
        data = response.json()
        for result in data["results"]:
            titles_list[result["title"]] = [result["release_date"], result["id"]]
        return render_template("select.html", titles=titles_list)
    return render_template("add.html", form=form)


@app.route("/select", methods=["GET", "POST"])
def select():
    movie_id = request.args.get("id")
    params = {"api_key": moviedb_api_key}
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?", params=params)
    response.raise_for_status()
    data = response.json()
    year = data["release_date"].split()[0]
    add_movie = Movie(
        title=data["title"],
        year=data["release_date"].split()[0],
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/original{data['poster_path']}"
    )
    db.session.add(add_movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
