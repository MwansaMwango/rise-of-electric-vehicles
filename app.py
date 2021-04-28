from flask import Flask, render_template, redirect, request, jsonify
import pprint
import time
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
# import scrape_telsa_data TBC - may not be required since data is already loaded in MongoDB

# Create an instance of our Flask app.
# Static folder has files inside reachable for everyone.
app = Flask(__name__) 

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")

#################################################
# Flask Routes
#################################################

# Send static files based on path location
# @app.route('/<path:path>')
# def static_file(path):
#     return app.send_static_file(path)

# Set route - displays landing page
@app.route("/")
def index():
    return render_template("index.html")

# Set route - displays US EV Model Sales
@app.route("/global-emissions")
def globalEmissions():
    return render_template("electricity_production.html")

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


if __name__ == "__main__":
    app.run(debug=True)
