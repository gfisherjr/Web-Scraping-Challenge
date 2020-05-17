from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars_info=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_info = scrape_mars.scrape()
    mars.update({}, mars_info, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)