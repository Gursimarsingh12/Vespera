from fastapi import APIRouter, Query
from Backend.controllers.iotpred import predict_consumption
from controllers.projectController import getAllProjects, getProjectsByLocation




router = APIRouter(
    tags=["devices"],
    responses={404: {"description": "Not found"}}
)

@router.post("/init-devices")
async def init_device(rooms : int = Query(), bulbs : int = Query(), fans : int = Query(), ovens : int = Query(), washing_machines : int = Query(), acs : int = Query()):
    return await predict_consumption(rooms, bulbs, fans, ovens, washing_machines, acs)


