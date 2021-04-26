from flask import Flask, render_template, redirect, jsonify
import pprint
import time
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# import scrape_telsa_data TBC - may not be required since data is already loaded in MongoDB

# Create an instance of our Flask app.
# Set a folder as static path so that the files inside are reachable for everyone.
# static_url_path='/static' is default as of 2020
app = Flask(__name__, static_url_path='/static') 

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")

#################################################
# Flask Routes
#################################################

# Set route - displays landing page
@app.route("/")
def index():
    return redirect("index.html")

# Send static files
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

# Get EV Sales data from MongoDB database
@app.route("/api/us-sales")
def getUsSales():
    all_sales = {}
  # After you first set of iterations over documents the cursor is used up. It's a read-once container.
  # Convert to list to avoid this.
    us_ev_sales_coll = list(mongo.db.us_ev_sales.find({}))

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

    response = jsonify(all_sales)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get Tesla Sales data from MongoDB database
@app.route("/api/v1/resources/tesla-sales")
def api_tesla_sales():
  # After you first set of iterations over documents the cursor is used up. It's a read-once container.
  # Convert to list to avoid this.
    tesla_sales_coll = list(mongo.db.tesla_production_sales.find({}))
    qtr_tesla_sales_dict_list = []
    for document in tesla_sales_coll: 
        qtr_tesla_sales_dict = {}
        qtr_tesla_sales_dict["Quarter"] = document['Quarter']
        qtr_tesla_sales_dict["Total_Sales"] = document['Total_Sales']
        qtr_tesla_sales_dict_list.append(qtr_tesla_sales_dict)
    
    response = jsonify(qtr_tesla_sales_dict_list) 
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)
