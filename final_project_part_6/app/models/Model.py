import joblib
import os
import pandas as pd
import numpy as np
import sklearn

class Model:
    def __init__(self, version):
        self.version = version
        self.model_path = os.path.join(os.getcwd(),"models","model_v"+self.version+".joblib")

    def transform(self,user_data):
        return True

    def validate(self,user_data):
        return True
        """if (transform(user_data)):
                                    return True Рудимент
                                else:
                                    return False"""

    def predict(self,user_data):
        loaded_model = joblib.load(self.model_path)
        user_data = pd.read_json(user_data, orient="split")
        if (self.version == "2"):
            prediction = loaded_model.predict(user_data)
            y_pred = prediction
            y_pred = y_pred[0]

            if (y_pred < 0):
                return "Увы мы не можем предложить вам скидки."
            elif (y_pred < 10):
                return "Мы можем предложить вам купить игру по скидке 50%"
            elif (y_pred < 25):
                return "Мы можем предложить вам купить игру по скидке 25%"
            elif (y_pred < 100):
                return "Мы можем предложить вам купить игру по скидке 10%"
            elif (y_pred < 1000):
                return "Мы можем предложить вам купить игру по скидке 5%"
            else:
                return "Увы мы не можем предложить вам скидки."
        else:
            y_pred = loaded_model.predict(user_data)
            top_5_indices = np.argsort(y_pred)[-5:][::-1]
            return ','.join(map(str, list(top_5_indices)))
    
    def __str__(self):
        return f"version = {self.version}"

    def get_version(self):
        return self.version