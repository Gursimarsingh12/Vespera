# predict.py

import pandas as pd
import joblib

def predict_consumption(rooms, bulbs, fans, ovens, washing_machines, acs):
    """Predict energy consumption for given inputs"""
        # Load model and features
    model = joblib.load('ml\energy_model.joblib')
    features = joblib.load('ml\model_features.joblib')
        
    # Prepare input data
    input_data = pd.DataFrame([{
        'rooms': rooms,
        'bulb_count': bulbs,
        'fan_count': fans,
        'oven_count': ovens,
        'washing_machine_count': washing_machines,
        'ac_count': acs
    }])
        
        # Make prediction
    daily_kwh = model.predict(input_data)[0]
    monthly_kwh = daily_kwh * 30
    monthly_cost = monthly_kwh * 0.12
        
    print(f"\nPrediction for {rooms} room setup:")
    print(f"Devices: {bulbs} bulbs, {fans} fans, {ovens} ovens, {washing_machines} washing machines, {acs} ACs")
    print(f"Daily Usage: {daily_kwh:.2f} kWh")
    print(f"Monthly Usage: {monthly_kwh:.2f} kWh")
    print(f"Estimated Monthly Cost: ${monthly_cost:.2f}")
        
    return daily_kwh, monthly_kwh, monthly_cost
        


