from flask import Flask, render_template, redirect, jsonify
import pprint
import time
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# import scrape_telsa_data TBC - may not be required since data is already loaded in MongoDB

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")

# Query DB for all relevant data to be used to initialise pages
tesla_prod_sales_coll = mongo.db.tesla_production_sales.find({})
# print("Tesla data", tesla_prod_sales_obj)
# for document in tesla_prod_sales_obj: pprint.pprint(document)

     

#################################################
# Flask Routes
#################################################

# Set route - displays landing page
@app.route("/")
def index():
    return render_template("index.html", tesla_prod_sales_data=tesla_prod_sales_coll)

# Set route - displays race chart
@app.route("/race_chart")
def raceChart():
    return render_template("race_chart.html")

# Get EV Sales data from MongoDB database
@app.route("/api/us-sales")
def getUsSales():
    all_sales = {}
  # After you first set of iterations over documents the cursor is used up. It's a read-once container.
  # Convert to list to avoid this.
    us_ev_sales_coll = list(mongo.db.us_ev_sales.find({}))
    # time.sleep(2)

    for year in range(2011,2020):
        vehicle_sales_dict_list = []
        for document in us_ev_sales_coll: 
            print("YEAR",year)  
            if document['Vehicle'] != 'Total':
                vehicle_sales_dict = {}
                vehicle_sales_dict["vehicle"] = document['Vehicle']
                vehicle_sales_dict["sales"] = document[str(year)]
                vehicle_sales_dict_list.append(vehicle_sales_dict)
        all_sales[year] = vehicle_sales_dict_list

    return jsonify(all_sales) 

    # return render_template("race_chart.html", us_ev_sales_data=us_ev_sales_data)

if __name__ == "__main__":
    app.run(debug=True)
