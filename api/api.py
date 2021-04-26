# API Engine for the Electric Vehicles data project

import flask
from flask import request, jsonify
from flask_pymongo import PyMongo
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")

# Default route - display helpful information
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Electric Vehicles API</h1>
<p>An API engine for the Electric Vehicles project.</p>
<br><p>API List'''


# A route to return all of the available copuntry codes in our catalogue.
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
    
# A route to return all of the available electricy production values in our catalogue.
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

@app.route('/api/v1/resources/electricity_production_values/country', methods=['GET'])
def api_id():
    # Check if a Country Code was provided as part of the URL.
    # If ID is provided, lookup the Country Name from Countries collection
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        country_code = mongo.db.country_codes.find({"Code": str(request.args['id'])})
        print(country_code[0]['Name'], file=sys.stderr)
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


app.run()