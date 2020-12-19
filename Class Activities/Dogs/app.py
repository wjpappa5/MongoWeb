# import necessary libraries
from flask import Flask, render_template

# @TODO: Initialize your Flask app here
app = Flask(__name__)

@app.route("/")
def index():
    dog_list = [{"Name": "Fido", "Type":"Poodle"},{"Name": "Binks", "Type":"Pitbull"},{"Name": "Savannah", "Type":"Golden Lab"},{"Name": "Max", "Type":"Chocolate Lab"}]
    return render_template("index.html", list=dog_list)

if __name__ == "__main__":
    app.run(debug=True)
