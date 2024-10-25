from fastapi import APIRouter, Query
from controllers.projectController import getAllProjects, getProjectsByLocation




router = APIRouter(
    tags=["projects"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-all-projects")
async def get_all_projects():
    return await getAllProjects()

@router.get("/get-projects-by-location")
async def get_projects_by_location(location: str = Query()):
    return await getProjectsByLocation(location)

