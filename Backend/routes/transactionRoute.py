from fastapi import APIRouter, Query
from controllers.stocksTransactionController import addFunds, buyShare, sellShare



router = APIRouter(
    tags=["transaction"],
    responses={404: {"description": "Not found"}}
)

@router.get("/buy-share")
async def get_all_projects(phone_num : int = Query() , share_id : int = Query(),amount : int = Query()):
    return await buyShare(phone_num , share_id, amount)

@router.get("/sell-share")
async def get_projects_by_location(phone_num : int = Query() , share_id : int = Query()  , amount : int = Query()):
    return await sellShare(phone_num , share_id, amount)

@router.get("/add-funds")
async def addFundsInWallet(phone_num : int = Query() , amount : float = Query(), ):
    return await addFunds(phone_num , amount)
