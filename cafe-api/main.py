from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random_cafe", methods=["GET"])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


# HTTP GET - Read Record
@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    all_cafes = []
    for cafe in cafes:
        all_cafes.append(cafe.to_dict())
    return jsonify(cafes=all_cafes)


@app.route("/search")
def get_cafe():
    location = request.args.get("location")
    cafe = db.session.query(Cafe).filter_by(location=location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    return jsonify(error={"Not Found": "Sorry, there is no cafe registered at that location"})


# HTTP POST - Create Record
@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form["name"],
        map_url=request.form["map_url"],
        img_url=request.form["img_url"],
        location=request.form["location"],
        seats=request.form["seats"],
        has_toilet=bool(request.form["has_toilet"]),
        has_wifi=bool(request.form["has_wifi"]),
        has_sockets=bool(request.form["has_sockets"]),
        can_take_calls=bool(request.form["can_take_calls"]),
        coffee_price=request.form["coffee_price"]
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    price = request.args.get("new_price")
    if cafe:
        cafe.coffee_price = price
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    return jsonify(error={"Not Found": "Sorry, there is no cafe with that id registered at our database"}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        if request.args.get("api_key") == "TopSecretApiKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully reported the closed cafe."}), 200
        else:
            return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api key "), 403
    return jsonify(error={"Not Found": "Sorry, there is no cafe with that id registered at our database"}), 404


if __name__ == '__main__':
    app.run(debug=True)
