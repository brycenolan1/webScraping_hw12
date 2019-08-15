from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    all_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=all_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_data_records = scrape_mars.scrape()
    mars_data.update({}, mars_data_records, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)