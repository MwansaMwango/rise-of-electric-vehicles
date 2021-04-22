from flask import Flask, render_template, redirect
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# import scrape_telsa_sales_wiki

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_db")

# Set route - displays first entry in MongoDB
@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)

# Scrape page and store info in MongoDB database
@app.route("/scrape")
def scrape():
    # Get mars data returned in results dictionary after running the scrape() function 
    mars_data = scrape_mars.scrape()
    # Create and update table caled 'collection' in mission_to_mars_db
    mongo.db.collection.update({}, mars_data, upsert=True)
    print("Scraped!", mars_data)
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)