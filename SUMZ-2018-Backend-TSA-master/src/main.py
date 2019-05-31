from flask import Flask, request, abort, jsonify
from sarima import predict
import dtos
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
    
    tsaRequest = TSARequest()
    tsaResponse = TSAResponse()
    
    try:
        #this is to validate the request
        check(json, loadSchema(schemaFileName))
        
        tsaRequest.TimeSeriesID = json[JsonRequestKeys.TimeSeriesID.value]
        tsaRequest.TimeSeriesValues = json[JsonRequestKeys.TimeSeriesValues.value]
        tsaRequest.PredictionSteps = json[JsonRequestKeys.PredictionSteps.value]
    except FileNotFoundError:
        abort(500, "schema for request validation not found")
    except Exception:
        abort(400, "invalid json input")
        
    try:
        tsaRequest.Order = json[JsonRequestKeys.Order.value]

        try:
            tsaRequest.SeasonalOrder = json[JsonRequestKeys.SeasonalOrder.value]
            
            try:
                #creating the model with the predict function of the sarima.py
                tsaResponse.Forecast = predict(timeSeriesID=tsaRequest.TimeSeriesID, timeSeriesValues=tsaRequest.TimeSeriesValues, pred_steps=tsaRequest.PredictionSteps, order=tsaRequest.Order, seasonalOrder=tsaRequest.SeasonalOrder)
            except Exception as e:
                abort(500, "Error during modeling process - " + str(e))
                
        except Exception:
            try:
                #creating the model with the predict function of the sarima.py
                tsaResponse.Forecast = predict(timeSeriesID=tsaRequest.TimeSeriesID, timeSeriesValues=tsaRequest.TimeSeriesValues, pred_steps=tsaRequest.PredictionSteps, order=tsaRequest.Order)
            except Exception as e:
                abort(500, "Error during modeling process - " + str(e))
        
    except Exception:
        try:
            tsaRequest.SeasonalOrder = json[JsonRequestKeys.SeasonalOrder.value]
            
            try:
                #creating the model with the predict function of the sarima.py
                tsaResponse.Forecast = predict(timeSeriesID=tsaRequest.TimeSeriesID, timeSeriesValues=tsaRequest.TimeSeriesValues, pred_steps=tsaRequest.PredictionSteps, seasonalOrder=tsaRequest.SeasonalOrder)
            except Exception as e:
                abort(500, "Error during modeling process - " + str(e))
                
        except Exception:
            try:
                #creating the model with the predict function of the brownRozeff.py
                tsaResponse.Forecast = predict(timeSeriesID=tsaRequest.TimeSeriesID, timeSeriesValues=tsaRequest.TimeSeriesValues, pred_steps=tsaRequest.PredictionSteps)
            except Exception as e:
                abort(500, "Error during modeling process - " + str(e))

    #returning the result as json
    return jsonify(id=tsaResponse.TimeSeriesID, forecast=tsaResponse.Forecast)

@app.errorhandler(Exception)
def global_exception_handler(error):
    return f'{error}', 500


if __name__ == "__main__":
    app.run(debug=True)
