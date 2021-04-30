from flask import Flask, render_template, redirect, request, jsonify
import pprint
import time
from flask.templating import render_template_string
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# import scrape_telsa_data TBC - may not be required since data is already loaded in MongoDB
import random

# Create an instance of our Flask app.
# Static folder has files inside reachable for everyone.
app = Flask(__name__) 

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")

#################################################
# Flask Routes
#################################################

# Set route - displays landing page
@app.route("/")
def index():
    return render_template("index.html")

# Set route - displays Global electricity production
@app.route("/global-emissions")
def globalEmissions():
    return render_template("electricity_production.html")

# Set route - displays Global charge station
@app.route("/global-charge-stations")
def globalChargeStations():
    return render_template("ev_charging_stations.html")

# Set route - displays US EV Model Sales
@app.route("/race-chart")
def raceChart():
    return render_template("race_chart.html")

# Set route - displays Tesla EV Sales
@app.route("/tesla-sales")
def teslaSales():
    return render_template("tesla_sales.html")

# Get US EV Sales data from MongoDB database
@app.route("/api/v1/resources/us-sales", methods = ['GET'])
def api_us_sales():
    all_sales = {}
  # After you first set of iterations over documents the cursor is used up. It's a read-once container.
  # Convert to list to avoid this.
    us_ev_sales_coll = list(mongo.db.us_ev_sales.find({}))

    for year in range(2011,2020):
        vehicle_sales_dict_list = []
        for document in us_ev_sales_coll: 
            if document['Vehicle'] != 'Total': #exclude the total column
                vehicle_sales_dict = {}
                vehicle_sales_dict["vehicle"] = document['Vehicle']
                vehicle_sales_dict["sales"] = document[str(year)]
                vehicle_sales_dict_list.append(vehicle_sales_dict)
        all_sales[year] = vehicle_sales_dict_list

    response = jsonify(all_sales)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get Tesla Sales data from MongoDB database
@app.route("/api/v1/resources/tesla-sales", methods = ['GET'])
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

# Get Global EV Market Share data from MongoDB database
@app.route("/api/v1/resources/market-share", methods = ['GET'])
def api_market_share():
    # Convert to list to avoid this.
    market_share_data = []
    # for doc in market_share_coll: 
    for doc in mongo.db.global_market_share.find(): 
        doc.pop('_id') 
        market_share_data.append(doc)
    response = jsonify(market_share_data) 
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get random EV Stats from MongoDB database
@app.route("/api/v1/resources/get-random-stat", methods = ['GET'])
def api_get_random_stat():
    # There are 40 quotes in one document in collection with keys from 0 to 39
    numStats = range(40)
    
    # Generate random integer from range
    rndStatKey = str(random.choice(numStats))
    
    # Create list to hold unpacked quotes
    ev_random_stats = []
    
    # Unpack docs in pymongo cursor 
    for doc in mongo.db.ev_random_stats.find(): 
        doc.pop('_id') 
        ev_random_stats.append(doc)
    
    # Get text from first and only doc using random generated key
    rndStatText = ev_random_stats[0][rndStatKey]
    
    response = jsonify(rndStatText) 
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# A route to return all of the available country codes in our Mongo catalogue.
@app.route('/api/v1/resources/countries/all', methods=['GET'])
def api_countries_all():
    docs = []
    # read records from Mongo, remove the _id field, convert to JSON and allow for CORS
    for doc in mongo.db.country_codes.find():
        doc.pop('_id') 
        docs.append(doc)
    response = jsonify(docs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
# A route to return all of the available electricity production values in our Mongo catalogue.
@app.route('/api/v1/resources/electricity_production_values/all', methods=['GET'])
def api_pv_all():
    docs = []
    # read records from Mongo, remove the _id field, convert to JSON and allow for CORS
    for doc in mongo.db.electricity_production_values.find():
        doc.pop('_id') 
        docs.append(doc)
    response = jsonify(docs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Return electricity production values for a single country in our Mongo catalogue.
@app.route('/api/v1/resources/electricity_production_values/country', methods=['GET'])
def api_electricity_prod_by_country_id():
    # Check if a Country Code was provided as part of the URL.
    # If ID is provided, lookup the Country Name from Countries collection
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        country_code = mongo.db.country_codes.find({"Code": str(request.args['id'])})
        # print(country_code[0]['Name'], file=sys.stderr)  # need to import sys library for debugging
        id = country_code[0]['Name']       
    else:
        return "Error: No id field provided. Please specify a country id."

    # read records from Mongo, remove the _id field, convert to JSON and allow for CORS
    docs = []
    for doc in mongo.db.electricity_production_values.find():
        doc.pop('_id') 
        if doc['country'] == id:
            docs.append(doc)

    response = jsonify(docs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# A route to return all charging location values in our Mongo catalogue.
@app.route('/api/v1/resources/ev_charging_station/all', methods=['GET'])
def api_charging_station_all():
    docs = []
    # read records from Mongo, remove the _id field, convert to JSON and allow for CORS
    for doc in mongo.db.charging_station.find():
        doc.pop('_id') 
        docs.append(doc)
    response = jsonify(docs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True)
