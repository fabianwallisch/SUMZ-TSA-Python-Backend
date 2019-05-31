from numpy import *
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import *

#created by Fabian Wallisch WWI16

def predict(timeSeriesValues, pred_steps, order, seasonal_order):
     
    #define the sarimax model; last param of seasonal order is frequency, e.g. 12=monthly
    #model = pmdarima.arima.ARIMA(timeSeriesValues, order=order, seasonal_order=seasonalOrder, with_intercept=True)
    model = SARIMAX(timeSeriesValues, order=order, seasonal_order=seasonal_order)
    
    #fitting the model, i.e. estimating the parameters
    model_fit = model.fit()
        
    #printing a summary of the model to the console
    print(model_fit.summary())
        
    return model_fit.forecast(pred_steps)
