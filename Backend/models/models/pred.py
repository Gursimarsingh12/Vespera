import pandas as pd
import joblib
import os

class SolarEnergyPredictorLoader:
    def __init__(self):
        self.monthly_models = {}
        model_dir = 'models'
        for month in range(1, 13):
            model_path = os.path.join(model_dir, f'solar_energy_model_month_{month}.pkl')
            self.monthly_models[f'month_{month}'] = joblib.load(model_path)
        
        preprocessor_path = os.path.join(model_dir, 'solar_energy_model_preprocessor.pkl')
        self.preprocessor = joblib.load(preprocessor_path)

    def predict_monthly_energy(self, input_features):
        X = pd.DataFrame([input_features])
        monthly_predictions = {}
        for month, model in self.monthly_models.items():
            monthly_predictions[month] = model.predict(X)[0]
        
        return monthly_predictions

def get_monthly_energy_predictions(location, panel_size_m2, panel_capacity_kw, panel_efficiency_percent, inverter_efficiency_percent, sunlight_hours):
    # Initialize the predictor loader
    predictor_loader = SolarEnergyPredictorLoader()

    # Define input features as a dictionary
    input_features = {
        'Location': location,
        'Panel_Size_m2': panel_size_m2,
        'Panel_Capacity_kW': panel_capacity_kw,
        'Panel_Efficiency_Percent': panel_efficiency_percent,
        'Inverter_Efficiency_Percent': inverter_efficiency_percent,
        'Sunlight_Hours': sunlight_hours
    }

    # Predict monthly energy production
    predictions = predictor_loader.predict_monthly_energy(input_features)
    
    return predictions

# Example usage:
location = 'Delhi'
panel_size_m2 = 25
panel_capacity_kw = 5
panel_efficiency_percent = 18
inverter_efficiency_percent = 95
sunlight_hours = 5

predictions = get_monthly_energy_predictions(location, panel_size_m2, panel_capacity_kw, panel_efficiency_percent, inverter_efficiency_percent, sunlight_hours)
print("Monthly Energy Predictions (kWh):")
print(predictions)