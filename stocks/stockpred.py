import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, Any

class SolarPredictor:
    def __init__(self, csv_path: str):
        """Initialize the predictor with CSV data"""
        self.scaler = StandardScaler()
        self.load_data(csv_path)
        
    def load_data(self, csv_path: str):
        """Load and process the CSV data"""
        try:
            self.projects_df = pd.read_csv(csv_path)
            month_columns = [f'Month_{i}_Energy_kWh' for i in range(1, 13)]
            
            # Calculate additional features
            self.projects_df['Summer_Generation'] = self.projects_df[[f'Month_{i}_Energy_kWh' for i in [5,6,7,8]]].mean(axis=1)
            self.projects_df['Winter_Generation'] = self.projects_df[[f'Month_{i}_Energy_kWh' for i in [11,12,1,2]]].mean(axis=1)
            self.projects_df['Generation_Variance'] = self.projects_df[month_columns].var(axis=1)
            
            # Add location-based rates
            location_rates = {
                'Gujarat': np.random.uniform(5.5, 6.2),
                'Delhi': np.random.uniform(6.8, 7.5),
                'Rajasthan': np.random.uniform(5.2, 6.0),
                'Kolkata': np.random.uniform(6.5, 7.2),
                'Hyderabad': np.random.uniform(6.0, 6.8),
                'Chennai': np.random.uniform(6.2, 7.0),
                'Mumbai': np.random.uniform(6.5, 7.3)
            }
            
            self.projects_df['Energy_Sale_Rate'] = self.projects_df['Location'].map(
                lambda x: location_rates.get(x, 6.0)
            )
            
            # Calculate costs
            location_base_costs = {
                'Gujarat': 42000,
                'Delhi': 48000,
                'Rajasthan': 40000,
                'Kolkata': 46000,
                'Hyderabad': 44000,
                'Chennai': 45000,
                'Mumbai': 50000
            }
            
            base_costs = self.projects_df['Location'].map(lambda x: location_base_costs.get(x, 45000))
            size_factor = 1 - (0.1 * np.log1p(self.projects_df['Panel_Capacity_kW']) / np.log1p(100))
            efficiency_factor = 1 + (self.projects_df['Panel_Efficiency_Percent'] - 15) / 100
            random_factor = np.random.uniform(0.925, 1.075, len(self.projects_df))
            
            self.projects_df['Cost_per_kW'] = base_costs * size_factor * efficiency_factor * random_factor
            self.projects_df['Total_Cost'] = self.projects_df['Panel_Capacity_kW'] * self.projects_df['Cost_per_kW']
            self.projects_df['Annual_Revenue'] = self.projects_df['Total_Annual_Energy_kWh'] * self.projects_df['Energy_Sale_Rate']
            self.projects_df['ROI'] = (self.projects_df['Annual_Revenue'] / self.projects_df['Total_Cost']) * 100
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
    
    def calculate_optimal_shares(self, project: Dict[str, Any], annual_consumption: float) -> Dict[str, Any]:
        """Calculate optimal share distribution for a project"""
        min_shares_needed = np.ceil(annual_consumption / (project['Total_Annual_Energy_kWh'] / 1000))
        base_shares = np.ceil(project['Panel_Capacity_kW'] * 2000)
        consumption_based_shares = min_shares_needed * 1.5
        
        total_shares = max(base_shares, consumption_based_shares)
        
        energy_per_share = project['Total_Annual_Energy_kWh'] / total_shares
        if energy_per_share < 0.5:
            total_shares = project['Total_Annual_Energy_kWh'] / 0.5
            
        energy_per_share = project['Total_Annual_Energy_kWh'] / total_shares
        required_shares = np.ceil(annual_consumption / energy_per_share)
        
        if total_shares <= required_shares:
            total_shares = required_shares * 1.3
            
        return {
            'total_shares': int(total_shares),
            'energy_per_share': project['Total_Annual_Energy_kWh'] / total_shares,
            'required_shares': int(required_shares),
            'share_cost': project['Total_Cost'] / total_shares
        }

    def predict_and_analyze(self, monthly_consumption: float) -> Dict[str, Any]:
        """
        Predict and analyze solar project details based on monthly consumption
        
        Args:
            monthly_consumption: Monthly energy consumption in kWh
            
        Returns:
            Dictionary containing all project analysis and recommendations
        """
        annual_consumption = monthly_consumption * 12
        
        # Calculate consumption coverage ratio
        coverage_ratio = self.projects_df['Total_Annual_Energy_kWh'] / annual_consumption
        
        # Calculate scores
        generation_score = 1 / (1 + np.abs(coverage_ratio - 1))
        efficiency_score = (self.projects_df['Panel_Efficiency_Percent'] + 
                          self.projects_df['Inverter_Efficiency_Percent']) / 200
        stability_score = 1 / (1 + self.projects_df['Generation_Variance'] / self.projects_df['Total_Annual_Energy_kWh'])
        roi_score = self.projects_df['ROI'] / 100
        
        # Calculate final score
        weights = {
            'generation': 0.3,
            'efficiency': 0.2,
            'stability': 0.2,
            'roi': 0.3
        }
        
        final_score = (
            weights['generation'] * generation_score +
            weights['efficiency'] * efficiency_score +
            weights['stability'] * stability_score +
            weights['roi'] * roi_score
        )
        
        # Get best project
        best_idx = final_score.idxmax()
        best_project = self.projects_df.iloc[best_idx]
        
        # Get monthly generation
        monthly_generation = [best_project[f'Month_{i}_Energy_kWh'] for i in range(1, 13)]
        
        # Calculate share details
        share_details = self.calculate_optimal_shares(best_project, annual_consumption)
        share_details['monthly_energy_per_share'] = [
            gen / share_details['total_shares'] for gen in monthly_generation
        ]
        share_details['shares_available'] = share_details['total_shares'] - share_details['required_shares']
        
        # Calculate monthly savings
        monthly_savings = [min(gen, monthly_consumption) * best_project['Energy_Sale_Rate'] 
                         for gen in monthly_generation]
        
        # Prepare results
        results = {
            'project_details': {
                'company': best_project['Company'],
                'location': best_project['Location'],
                'panel_capacity': best_project['Panel_Capacity_kW'],
                'cost_per_kW': best_project['Cost_per_kW'],
                'energy_sale_rate': best_project['Energy_Sale_Rate']
            },
            'generation_details': {
                'annual_generation': best_project['Total_Annual_Energy_kWh'],
                'monthly_generation': monthly_generation
            },
            'share_details': share_details,
            'financial_details': {
                'expected_roi': best_project['ROI'],
                'payback_years': best_project['Total_Cost'] / best_project['Annual_Revenue'],
                'monthly_savings': monthly_savings
            }
        }
        
        return results

def format_and_print_results(results: Dict[str, Any]) -> None:
    """Format and print the analysis results"""
    project = results['project_details']
    share_details = results['share_details']
    financial = results['financial_details']
    
    print("\nRecommended Project Details:")
    print(f"Company: {project['company']}")
    print(f"Location: {project['location']}")
    print(f"Panel Capacity: {project['panel_capacity']:.2f} kW")
    print(f"Cost per kW: ₹{project['cost_per_kW']:,.2f}")
    print(f"Energy Sale Rate: ₹{project['energy_sale_rate']:.2f}/kWh")
    
    print("\nShare Details:")
    print(f"Total Project Shares: {share_details['total_shares']:,}")
    print(f"Energy per Share (Annual): {share_details['energy_per_share']:.2f} kWh")
    print(f"Cost per Share: ₹{share_details['share_cost']:,.2f}")
    print(f"Required Shares for Your Consumption: {share_details['required_shares']:,}")
    print(f"Remaining Available Shares: {share_details['shares_available']:,}")
    
    print("\nFinancial Details:")
    print(f"Expected ROI: {financial['expected_roi']:.2f}%")
    print(f"Payback Period: {financial['payback_years']:.2f} years")
    
    print("\nMonthly Generation and Savings:")
    print("Month  |  Total Generation (kWh)  |  Per Share (kWh)  |  Expected Savings")
    print("-" * 70)
    for month, (gen, per_share, saving) in enumerate(zip(
        results['generation_details']['monthly_generation'],
        share_details['monthly_energy_per_share'],
        financial['monthly_savings']
    ), 1):
        print(f"{month:2d}     |  {gen:10.2f}            |  {per_share:8.2f}        |  ₹{saving:10,.2f}")

# Example usage:

# Initialize the predictor with CSV data
predictor = SolarPredictor('solar_installation_analysis_monthly.csv')

# Get analysis for a specific monthly consumption
monthly_consumption = float(input("Enter your monthly consumption in kWh: "))
results = predictor.predict_and_analyze(monthly_consumption)

# Print the results
format_and_print_results(results)
