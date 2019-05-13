from flask import Flask, request, abort, jsonify
from brownRozeff import predict
from dtos import JsonRequestKeys
from checkRequest import check, loadSchema

#modified by Fabian Wallisch WWI16

app = Flask(__name__)
#This is the file name of the schema that is used to validate time series analysis requests
schemaFileName = "requestSchema.json"

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/predict", methods=['POST'])
def make_predictions():
    json = request.get_json()
    
    try:
        #this is to validate the request
        check(json, loadSchema(schemaFileName))
    except FileNotFoundError:
        abort(500, "schema for request validation not found")
    except Exception:
        abort(400, "invalid json input")
    
    time_series = json[JsonRequestKeys.TimeSeries.value]
    pred_steps = json[JsonRequestKeys.PredictionSteps.value]
    num_samples = json[JsonRequestKeys.NumberOfSamples.value]

    response = {}
    
    try:
        #creating the model with the predict function of the brownRozeff.py
        result = predict(time_series=time_series, pred_steps=pred_steps, num_samples=num_samples)
        response['timeSeries'] = result
    except Exception as e:
        abort(500, "Error during modeling process - " + str(e))

    #returning the result as json
    return jsonify(response)

@app.errorhandler(Exception)
def global_exception_handler(error):
    return f'{error}', 500


if __name__ == "__main__":
    app.run(debug=True)
