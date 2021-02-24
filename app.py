# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb+srv://mongodb:Ankaja99!@cluster0.izpbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
    mars_dict = {}
    # Run scrapped functions
    mars_db = mongo.db.mars_info
    mars_dict["news_title"],mars_dict["news_p"] = scrape_mars.scrape_mars_news()
    mars_dict["featured_image_url"] = "https://www.nasa.gov/sites/default/files/thumbnails/image/rover_drop.jpg"
    mars_dict["mars_facts"] = scrape_mars.scrape_mars_facts()
    # mars_dict["mars_weather"] = scrape_mars.scrape_mars_weather()
    mars_dict["hemispheres_info"] = scrape_mars.scrape_mars_hemispheres()
    mars_db.update({}, mars_dict, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

