from enum import Enum

class JsonRequestKeys(Enum):
    TimeSeriesID = 'id'
    TimeSeriesValues = 'values'
    PredictionSteps = 'predSteps'
    Order = 'order'
    SeasonalOrder = 'seasonalOrder'
    
class TSARequest():
    
    def __init__(self):
        self.TimeSeriesID = ""
        self.TimeSeriesValues = []
        self.PredictionSteps = 0
        self.Order = []
        self.SeasonalOrder = []
    
class TSAResponse():
    
    def __init__(self):
        self.TimeSeriesID = ""
        self.Forecast = []
