from numpy import *
import statsmodels.api as sm

#created by Fabian Wallisch WWI16

def predict(time_series, pred_steps, num_samples):
    result = []

    for x in range(len(time_series)):
        result.append({})
        result[x]['id'] = time_series[x]['id']
        result[x]['preds'] = []

        train_series = array(time_series[x]['values'])
        
        #define the sarimax model; first param of seasonal order is frequency, e.g. 12=monthly
        model = sm.tsa.SARIMAX(train_series, order=(1,0,0), seasonal_order=(0,1,1,4), enforce_stationarity=False, enforce_invertibility=False)

        #fitting the model, i.e. estimating the parameters
        try:
            model_fit = model.fit()
        #if too few observations are available, the start parameters have to be defined manually
        except ValueError:
            print("Maxlag error, too few observations")
            mod.fit([0,0,1.])
        
        #printing a summary of the model to the console
        print(model_fit.summary())
        
        #providing multiple samples of the resulting forecast
        for i in range(num_samples):
            model_forecast = model_fit.forecast(pred_steps)
            result[x]['preds'].append(list(model_forecast))

    return result
