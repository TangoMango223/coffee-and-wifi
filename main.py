from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, URL
import csv
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeForm(FlaskForm):
    # Preset rating icons
    coffee_list = ["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
    wifi_list = ["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
    power_list = ["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]

    #The questions that will be asked
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL(message = "Invalid URL. Please make sure it has to type the https:// portion.")])
    opentime = StringField('Opening Time', validators=[DataRequired()])
    closingtime = StringField('Opening Time', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=coffee_list, default=1)
    wifi_rating = SelectField("Wifi Rating", choices=wifi_list, default=1)
    power_rating = SelectField("Power Rating", choices=power_list, default=1)

    # Submission:
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# Solution to adding dropdown from list: https://stackoverflow.com/questions/46047658/how-to-add-a-drop-down-with-valuespre-defined-in-flask-app-models
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods = ["GET", "POST"])
def add_cafe():
    form = CafeForm()
    n_message = "Add a new cafe into the database"

    # with   if form.validate_on_submit()
    if form.validate_on_submit():
        n_message = "Thanks! Feel free to keep going and add more."
        # Retrieve the results
        result_list = [str(form.cafe.data), str(form.location.data),
                str(form.opentime.data), str(form.closingtime.data),
                str(form.coffee_rating.data), str(form.wifi_rating.data),
                str(form.power_rating.data)
                ]

        # Open file, write to it and close - we want to use "a" mode since we are adding on.
        with open("cafe-data.csv", mode= "a") as file:
            # create the writer:
            full_entry = ""
            for item in result_list:
                addition = f"{item},"
                full_entry += addition
            print(full_entry)

            file.write(f"\n{full_entry}")

        return render_template('add.html', form=form, message=n_message)

    # Exercise:
    # Make the form write a new row into cafe-data.csv

    # End of the code
    return render_template('add.html', form=form, message = n_message)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    # Remove the first entry, since it's just headers
    del list_of_rows[0]

    # Calculate number of dimensions:
    num_dimensions = len(list_of_rows[0])

    return render_template('cafes.html', cafes=list_of_rows, n_dim = num_dimensions)


if __name__ == '__main__':
    app.run(debug=True)
