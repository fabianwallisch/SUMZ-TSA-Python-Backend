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
        
        #first param of seasonal order is frequency, e.g. 12=monthly
        model = sm.tsa.SARIMAX(train_series, order=(1,0,0), seasonal_order=(0,1,1,4), enforce_stationarity=False, enforce_invertibility=False)

        model_fit = model.fit()
        
        print(model_fit.summary())
        
        for i in range(num_samples):
            model_forecast = model_fit.forecast(pred_steps)
            result[x]['preds'].append(list(model_forecast))

    return result