# import main Flask class and request object
from flask import Flask, request
import pandas as pd
from car_finder_api import find_car


df_cars = pd.read_csv("vehicles.csv", low_memory=False)

# create the Flask app
app = Flask(__name__)

@app.route('/')
def rootRoute():
    return "Welcome"  

@app.route('/cars')
def car_finder():
    make = request.args.get("make")
    model = request.args.get("model")
    year = request.args.get("year")
    
    result = find_car(f"{make} {model} {year}", df_cars).to_dict(orient='records')

    return result[0], 200  # return data and 200 OK code

@app.route('/query-example')
def query_example():
    return 'Query String Example'

@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    return 'Form Data Example'

@app.route('/json-example')
def json_example():
    return 'JSON Object Example'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)