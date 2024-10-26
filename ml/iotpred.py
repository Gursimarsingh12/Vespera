# predict.py

import pandas as pd
import joblib

def predict_consumption(rooms, bulbs, fans, ovens, washing_machines, acs):
    """Predict energy consumption for given inputs"""
        # Load model and features
    model = joblib.load('energy_model.joblib')
    features = joblib.load('model_features.joblib')
        
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
        



    
    # Example usage
# print("\n1. Small Studio")
predict_consumption(rooms=1, bulbs=3, fans=1, ovens=1, washing_machines=1, acs=1)
    
print("\n2. Medium Apartment")
predict_consumption(rooms=2, bulbs=5, fans=2, ovens=1, washing_machines=1, acs=1)
    
print("\n3. Large House")
predict_consumption(rooms=4, bulbs=10, fans=4, ovens=1, washing_machines=1, acs=3)

