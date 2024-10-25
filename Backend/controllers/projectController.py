from bson import ObjectId  # Import ObjectId for handling MongoDB ObjectIds
from models.projectSchema import Project
from controllers.databaseController import client
from fastapi import HTTPException
from .databaseController import getProjectCollection

def serialize_document(doc):
    """Convert MongoDB document to JSON serializable format."""
    doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return doc

async def getAllProjects():
    try:
        project_collection = await getProjectCollection()
        projects_cursor = project_collection.find()
        
        # Convert cursor to a list of dictionaries and serialize each document
        projects = [serialize_document(project) for project in await projects_cursor.to_list(length=None)]
        
        return projects  # Directly return the list of projects
    except Exception as e:
        print(f"Error fetching projects: {e}")
        raise HTTPException(status_code=500, detail="Error fetching projects")
    
async def getProjectsByLocation(location: str):
    try:
        project_collection = await getProjectCollection()
        projects_cursor = project_collection.find({"project_location": location})
        
        # Convert cursor to a list of dictionaries and serialize each document
        projects = [serialize_document(project) for project in await projects_cursor.to_list(length=None)]
        
        # Sort the projects based on expected ROI in descending order
        projects.sort(key=lambda x: x["expected_roi"], reverse=True)
        
        return projects  # Directly return the list of projects
    except Exception as e:
        print(f"Error fetching projects by location: {e}")
        raise HTTPException(status_code=500, detail="Error fetching projects by location")
