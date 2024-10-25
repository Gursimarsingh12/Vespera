from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict
import random

class Project(BaseModel):
    project_id: str
    project_company: str
    project_location: str
    project_size: float  # Total project size in MW
    installed_capacity: float  # Installed capacity in MW
    operational_capacity: float  # Operational capacity in MW
    project_cost: float  # Total project cost in crores
    project_status: str
    project_subscription_cost: float  # in INR per share
    expected_roi: float  # Expected return on investment in %
    sunlight_hours_per_day: float  # Avg sunlight per day at the location
    maintenance_cost: float  # Annual maintenance cost in crores
    annual_carbon_offset: float  # Estimated annual carbon offset in tons
    peak_efficiency: float  # Maximum efficiency of the project in %
    degradation_rate: float  # Yearly degradation rate of solar panels in %
    estimated_output: float  # Estimated annual energy output in MWh
    estimated_returns_per_share: float  # Estimated returns per share in INR
    earnings_per_share: float  # Earnings per share in INR
    subscriptions_accepted: int  # Number of subscriptions accepted
    active_subscribers: int  # Number of active subscribers

class ProjectHolding(BaseModel):
    project_id: str
    num_shares: int
    share_price: float  # Initial share price
    total_investment: float  # Total investment by the user
    profit: Dict[str, float]  # Dictionary with keys for monthly, quarterly, and annual profit
    carbon_offset: float  # Carbon offset per share
    purchase_date: datetime
    projected_annual_return: float  # Expected annual return for the holding
    current_share_value: float  # Current market value per share