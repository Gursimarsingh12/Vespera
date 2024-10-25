from uuid import UUID
from controllers.databaseController import get_users_collection, getProjectCollection
from datetime import datetime
from models.projectSchema import ProjectHolding


async def buyShare(phone_num: int, share_id: str, amount: int):
    user_collection = await get_users_collection()
    existing_user = await user_collection.find_one({"phone_number": phone_num})

    project_collection = await getProjectCollection()
    project = await project_collection.find_one({"project_id": share_id})

    if existing_user is None:
        return {"message": "User not found"}
    
    if project is None:
        return {"message": "Project not found"}

    total_cost = project["project_subscription_cost"] * amount
    if existing_user["balance"] < total_cost:
        return {"message": "Insufficient funds"}

    # Deduct total cost from user's balance
    updated_balance = existing_user["balance"] - total_cost

    # Extract earnings per share for profit calculations
    earnings_per_share = project["earnings_per_share"]

    # Check if user already has holdings in this project
    active_stocks = existing_user.get("active_stocks", [])
    existing_holding = next((holding for holding in active_stocks if holding["project_id"] == share_id), None)

    if existing_holding:
        # Update existing holding
        existing_holding["num_shares"] += amount
        existing_holding["total_investment"] += total_cost
        existing_holding["profit"]["annual"] = earnings_per_share * existing_holding["num_shares"]
        existing_holding["profit"]["monthly"] = earnings_per_share * existing_holding["num_shares"] / 12
        existing_holding["profit"]["quarterly"] = earnings_per_share * existing_holding["num_shares"] / 4
        existing_holding["carbon_offset"] += project["annual_carbon_offset"] / project["project_size"] * amount
    else:
        # Create new holding entry
        new_holding = ProjectHolding(
            project_id=project["project_id"],
            num_shares=amount,
            share_price=project["project_subscription_cost"],
            total_investment=total_cost,
            profit={
                "monthly": earnings_per_share * amount / 12,  # Monthly revenue from project per share
                "quarterly": earnings_per_share * amount / 4,  # Quarterly revenue
                "annual": earnings_per_share * amount  # Annual revenue
            },
            carbon_offset=project["annual_carbon_offset"] / project["project_size"] * amount,
            purchase_date=datetime.utcnow(),
            projected_annual_return=project["expected_roi"],
            dividend_yield=0.0,  
            current_share_value=project["project_subscription_cost"]
        )
        active_stocks.append(new_holding.dict())

    # Update user document
    await user_collection.update_one(
        {"phone_number": phone_num},
        {
            "$set": {
                "balance": updated_balance,
                "active_stocks": active_stocks
            }
        }
    )

    return {
        "message": "Shares purchased successfully",
        "amount_purchased": amount,
        "updated_balance": updated_balance
    }


async def sellShare(phone_num: int, share_id: str, amount: int):
    user_collection = await get_users_collection()
    existing_user = await user_collection.find_one({"phone_number": phone_num})

    project_collection = await getProjectCollection()
    project = await project_collection.find_one({"project_id": share_id})

    if existing_user is None:
        return {"message": "User not found"}
    
    if project is None:
        return {"message": "Project not found"}

    # Check if user owns the specified share
    active_stocks = existing_user.get("active_stocks", [])
    existing_holding = next((holding for holding in active_stocks if holding["project_id"] == share_id), None)

    if existing_holding is None:
        return {"message": "User does not own shares of this project"}

    # Check if user has enough shares to sell
    if existing_holding["num_shares"] < amount:
        return {"message": "Insufficient shares to sell"}

    # Calculate earnings based on current share value and revenue per share
    total_earnings = existing_holding["current_share_value"] * amount
    earnings_per_share = project["earnings_per_share"]

    # Update the user's balance
    updated_balance = existing_user["balance"] + total_earnings + (earnings_per_share * amount)

    # Update or remove the holding
    if existing_holding["num_shares"] == amount:
        active_stocks = [holding for holding in active_stocks if holding["project_id"] != share_id]
    else:
        # Update holding details if only some shares are sold
        existing_holding["num_shares"] -= amount
        existing_holding["total_investment"] -= existing_holding["share_price"] * amount
        existing_holding["profit"]["annual"] = earnings_per_share * existing_holding["num_shares"]

    # Update user document in the database
    await user_collection.update_one(
        {"phone_number": phone_num},
        {
            "$set": {
                "balance": updated_balance,
                "active_stocks": active_stocks
            }
        }
    )

    return {
        "message": "Shares sold successfully",
        "amount_sold": amount,
        "earnings_from_sale": total_earnings,
        "updated_balance": updated_balance
    }

async def addFunds(phone_num : int , amount : float):

    user_collection = await get_users_collection()
    existing_user = await user_collection.find_one({"phone_number": phone_num})

    if existing_user is None:
        return {"message": "User not found"}
    
    updated_balance = existing_user["balance"] + amount

    await user_collection.update_one(
        {"phone_number": phone_num},
        {
            "$set": {
                "balance": updated_balance
            }
        }
    )

    return {
        "message": "Funds added successfully",
        "amount_added": amount,
        "updated_balance": updated_balance
    }
