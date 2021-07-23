from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location (on Google Maps)', validators=[DataRequired(), URL(message="You need to "
                                                                                                     "provide a valid "
                                                                                                     "URL")])
    open = StringField('Opening time (eg. 08:00)', validators=[DataRequired()])
    close = StringField('Closing time (eg. 19:00)', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=[("☕"), ("☕☕"), ("☕☕☕"), ("☕☕☕☕"), ("☕☕☕☕☕")],
                         validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=[("💪🏼"), ("💪🏼💪🏼"), ("💪🏼💪🏼💪🏼"), ("💪🏼💪🏼💪🏼💪🏼"), ("💪🏼💪🏼💪🏼💪🏼💪🏼")],
                       validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=[("🔌"), ("🔌🔌"), ("🔌🔌🔌"), ("🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌")],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', mode="a", newline='') as csv_file:
            row_writer = csv.writer(csv_file)
            new_row = [form.cafe.data, form.location.data, form.open.data, form.close.data, form.coffee.data,
                       form.wifi.data, form.power.data]
            row_writer.writerow(new_row)
            return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
