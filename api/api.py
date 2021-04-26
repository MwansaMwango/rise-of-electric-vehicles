import flask
from flask import request, jsonify
from flask_pymongo import PyMongo

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/electric_vehicles")


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Electric Vehicles API</h1>
<p>A prototype API for the Electric Vehicles project.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/countries/all', methods=['GET'])
def api_countries_all():
    docs = []
    for doc in mongo.db.country_codes.find():
        doc.pop('_id') 
        docs.append(doc)
    return jsonify(docs)
    

@app.route('/api/v1/resources/electricity_production_values/all', methods=['GET'])
def api_pv_all():
    docs = []
    for doc in mongo.db.electricity_production_values.find():
        doc.pop('_id') 
        docs.append(doc)
    return jsonify(docs)

@app.route('/api/v1/resources/electricity_production_values/country', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    docs = []
    for doc in mongo.db.electricity_production_values.find():
        doc.pop('_id') 
        if doc['country'] == id:
            docs.append(doc)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    response = jsonify(docs)
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


app.run()