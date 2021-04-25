from flask import Flask, render_template, redirect
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# import scrape_telsa_data TBC - may not be required since data is already loaded in MongoDB

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")

# Query DB for all relevant data to be used to initialise pages
tesla_prod_sales_data = mongo.db.tesla_production_sales.find({})
print("Tesla data", tesla_prod_sales_data)
us_ev_sales_data = mongo.db.us_ev_sales.find({})
print("US EV Sales data", us_ev_sales_data)

# Set route - displays first entry in MongoDB
@app.route("/")
def index():
    return render_template("index.html", tesla_prod_sales_data=tesla_prod_sales_data)

# Scrape page and store info in MongoDB database
# @app.route("/")
# def scrape():
#     # Get mars data returned in results dictionary after running the scrape() function
#     mars_data = scrape_mars.scrape()
#     # Create and update table caled 'collection' in mission_to_mars_db
#     mongo.db.collection.update({}, mars_data, upsert=True)
#     print("Scraped!", mars_data)
#     # Redirect back to home page
#     return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
