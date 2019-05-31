from numpy import *
import statsmodels.api as sm
from pmdarima import *

#created by Fabian Wallisch WWI16

def predict(timeSeriesID, timeSeriesValues, pred_steps, order, seasonalOrder):
        
    #define the sarimax model; first param of seasonal order is frequency, e.g. 12=monthly
    model = pmdarima.arima.ARIMA(timeSeriesValues, order=order, seasonal_order=seasonalOrder, with_intercept=True)

    #fitting the model, i.e. estimating the parameters
    model_fit = model.fit()
        
    #printing a summary of the model to the console
    print(model_fit.summary())
        
    return model_fit.forecast(pred_steps)
