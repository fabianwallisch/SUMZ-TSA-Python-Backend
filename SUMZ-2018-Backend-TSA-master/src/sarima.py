from numpy import *
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import *

#created by Fabian Wallisch WWI16

def predict(timeSeriesValues, pred_steps, **kwargs):
    
    order = kwargs.get('order', None)
    seasonal_order = kwargs.get('seasonal_order', None)
    
    #define the sarimax model; last param of seasonal order is frequency, e.g. 12=monthly
    if order is None and seasonal_order is None:
        model = SARIMAX(timeSeriesValues, enforce_stationarity=False)
    if order is None and seasonal_order is not None:
        model = SARIMAX(timeSeriesValues, seasonal_order=seasonal_order, enforce_stationarity=False)
    if order is not None and seasonal_order is None:
        model = SARIMAX(timeSeriesValues, order=order, enforce_stationarity=False)
    if order is not None and seasonal_order is not None:
        model = SARIMAX(timeSeriesValues, order=order, seasonal_order=seasonal_order, enforce_stationarity=False)
     
    #model = pmdarima.arima.ARIMA(timeSeriesValues, order=order, seasonal_order=seasonalOrder, with_intercept=True)
    
    #fitting the model, i.e. estimating the parameters
    model_fit = model.fit()
        
    #printing a summary of the model to the console
    print(model_fit.summary())
        
    return model_fit.forecast(pred_steps)
