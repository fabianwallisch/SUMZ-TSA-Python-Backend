from flask import Flask, request, abort, jsonify
from sarima import predict
from dtos import TSARequest, TSAResponse, JsonRequestKeys
from checkRequest import check, loadSchema
import numpy

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
    
    tsaRequest = TSARequest()
    tsaResponse = TSAResponse()
    
    try:
        #this is to validate the request
        check(json, loadSchema(schemaFileName))
        
        tsaRequest.TimeSeriesID = json[JsonRequestKeys.TimeSeriesID.value]
        tsaRequest.TimeSeriesValues = json[JsonRequestKeys.TimeSeriesValues.value]
        tsaRequest.PredictionSteps = json[JsonRequestKeys.PredictionSteps.value]
        tsaRequest.Order = json[JsonRequestKeys.Order.value]
        tsaRequest.SeasonalOrder = json[JsonRequestKeys.SeasonalOrder.value]
    except FileNotFoundError:
        abort(500, "Schema for request validation not found")
    except Exception as e:
        abort(400, str(e))
        
    try:
        #creating the forecast with the predict function of the sarima.py
        tsaResponse.Forecast = predict(timeSeriesValues=tsaRequest.TimeSeriesValues, pred_steps=tsaRequest.PredictionSteps, order=tsaRequest.Order, seasonal_order=tsaRequest.SeasonalOrder)
    except Exception as e:
        abort(500, "Error during modeling process - " + str(e))

    #returning the result as json
    return jsonify(id=tsaResponse.TimeSeriesID, forecast=tsaResponse.Forecast.tolist())

@app.errorhandler(Exception)
def global_exception_handler(error):
    return f'{error}', 500


if __name__ == "__main__":
    app.run(debug=True)
