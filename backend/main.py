from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Dict, Any
import logging

from config import settings
from database import db
from models import (
    Entity, EntityResponse, Relationship, RelationshipResponse,
    EntityState, WorkflowDefinition, WorkflowExecution,
    GraphQuery, HealthResponse
)
from services.ontology_service import OntologyService
from services.workflow_service import WorkflowService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application"""
    logger.info("Starting application...")
    try:
        # Database connection will be established on first use (lazy loading)
        logger.info("Application ready - database connection will be established on first request")
        yield
    finally:
        logger.info("Shutting down application...")
        db.close()


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Ontology and Workflow Engine built on Snowflake",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ontology_service = OntologyService(db)
workflow_service = WorkflowService(db)


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Snowflake Ontology & Workflow Engine API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_DATABASE()")
        database = cursor.fetchone()[0]
        cursor.close()
        
        return HealthResponse(
            status="healthy",
            database=database,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


# ==================== Entity Endpoints ====================

@app.post("/entities", response_model=EntityResponse, status_code=201)
async def create_entity(entity: Entity):
    """Create a new entity in the ontology"""
    try:
        result = ontology_service.create_entity(entity)
        return result
    except Exception as e:
        logger.error(f"Error creating entity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/entities", response_model=List[EntityResponse])
async def list_entities(
    entity_type: str = None,
    limit: int = 100,
    offset: int = 0
):
    """List entities with optional filtering"""
    try:
        entities = ontology_service.list_entities(
            entity_type=entity_type,
            limit=limit,
            offset=offset
        )
        return entities
    except Exception as e:
        logger.error(f"Error listing entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    """Get a specific entity by ID"""
    try:
        entity = ontology_service.get_entity(entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        return entity
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting entity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/entities/{entity_id}", response_model=EntityResponse)
async def update_entity(entity_id: str, entity: Entity):
    """Update an existing entity"""
    try:
        result = ontology_service.update_entity(entity_id, entity)
        if not result:
            raise HTTPException(status_code=404, detail="Entity not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating entity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/entities/{entity_id}", status_code=204)
async def delete_entity(entity_id: str):
    """Delete an entity"""
    try:
        success = ontology_service.delete_entity(entity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Entity not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting entity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Relationship Endpoints ====================

@app.post("/relationships", response_model=RelationshipResponse, status_code=201)
async def create_relationship(relationship: Relationship):
    """Create a new relationship between entities"""
    try:
        result = ontology_service.create_relationship(relationship)
        return result
    except Exception as e:
        logger.error(f"Error creating relationship: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/relationships", response_model=List[RelationshipResponse])
async def list_relationships(
    entity_id: str = None,
    predicate: str = None,
    limit: int = 100
):
    """List relationships with optional filtering"""
    try:
        relationships = ontology_service.list_relationships(
            entity_id=entity_id,
            predicate=predicate,
            limit=limit
        )
        return relationships
    except Exception as e:
        logger.error(f"Error listing relationships: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/relationships/{relationship_id}", status_code=204)
async def delete_relationship(relationship_id: str):
    """Delete a relationship"""
    try:
        success = ontology_service.delete_relationship(relationship_id)
        if not success:
            raise HTTPException(status_code=404, detail="Relationship not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting relationship: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Graph Query Endpoints ====================

@app.post("/graph/query", response_model=Dict[str, Any])
async def query_graph(query: GraphQuery):
    """Query the ontology graph"""
    try:
        result = ontology_service.query_graph(query)
        return result
    except Exception as e:
        logger.error(f"Error querying graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/graph/stats", response_model=Dict[str, Any])
async def get_graph_stats():
    """Get statistics about the ontology graph"""
    try:
        stats = ontology_service.get_graph_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting graph stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Workflow Endpoints ====================

@app.post("/workflows", response_model=WorkflowDefinition, status_code=201)
async def create_workflow(workflow: WorkflowDefinition):
    """Create a new workflow definition"""
    try:
        result = workflow_service.create_workflow(workflow)
        return result
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows", response_model=List[WorkflowDefinition])
async def list_workflows(enabled: bool = None):
    """List workflow definitions"""
    try:
        workflows = workflow_service.list_workflows(enabled=enabled)
        return workflows
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/{workflow_id}", response_model=WorkflowDefinition)
async def get_workflow(workflow_id: str):
    """Get a specific workflow definition"""
    try:
        workflow = workflow_service.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return workflow
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecution)
async def execute_workflow(workflow_id: str, entity_id: str, input_data: Dict[str, Any] = None):
    """Manually execute a workflow"""
    try:
        result = workflow_service.execute_workflow(workflow_id, entity_id, input_data or {})
        return result
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/executions", response_model=List[WorkflowExecution])
async def list_workflow_executions(
    workflow_id: str = None,
    entity_id: str = None,
    limit: int = 100
):
    """List workflow executions"""
    try:
        executions = workflow_service.list_executions(
            workflow_id=workflow_id,
            entity_id=entity_id,
            limit=limit
        )
        return executions
    except Exception as e:
        logger.error(f"Error listing workflow executions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== State Management Endpoints ====================

@app.get("/entities/{entity_id}/state", response_model=EntityState)
async def get_entity_state(entity_id: str):
    """Get the current state of an entity"""
    try:
        state = workflow_service.get_entity_state(entity_id)
        if not state:
            raise HTTPException(status_code=404, detail="Entity state not found")
        return state
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting entity state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/entities/{entity_id}/state", response_model=EntityState)
async def update_entity_state(entity_id: str, new_state: str, state_data: Dict[str, Any] = None):
    """Update the state of an entity (triggers workflows)"""
    try:
        result = workflow_service.update_entity_state(entity_id, new_state, state_data or {})
        return result
    except Exception as e:
        logger.error(f"Error updating entity state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
