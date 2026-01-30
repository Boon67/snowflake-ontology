import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from database import SnowflakeConnection
from models import (
    WorkflowDefinition, WorkflowExecution, WorkflowStatus, EntityState
)


class WorkflowService:
    """Service for managing workflows and entity states"""
    
    def __init__(self, db: SnowflakeConnection):
        self.db = db
    
    def create_workflow(self, workflow: WorkflowDefinition) -> WorkflowDefinition:
        """Create a new workflow definition"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        workflow_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        cursor.execute("""
            INSERT INTO WORKFLOW_DEFINITIONS (
                WORKFLOW_ID, NAME, DESCRIPTION, TRIGGER_CONDITION,
                ACTION_TYPE, ACTION_CONFIG, ENABLED, CREATED_AT
            ) VALUES (%s, %s, %s, %s, %s, PARSE_JSON(%s), %s, %s)
        """, (
            workflow_id,
            workflow.name,
            workflow.description,
            workflow.trigger_condition,
            workflow.action_type,
            json.dumps(workflow.action_config),
            workflow.enabled,
            now
        ))
        
        conn.commit()
        cursor.close()
        
        workflow.workflow_id = workflow_id
        workflow.created_at = now
        return workflow
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Get a workflow definition by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT WORKFLOW_ID, NAME, DESCRIPTION, TRIGGER_CONDITION,
                   ACTION_TYPE, ACTION_CONFIG, ENABLED, CREATED_AT
            FROM WORKFLOW_DEFINITIONS
            WHERE WORKFLOW_ID = %s
        """, (workflow_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        return WorkflowDefinition(
            workflow_id=row[0],
            name=row[1],
            description=row[2],
            trigger_condition=row[3],
            action_type=row[4],
            action_config=json.loads(row[5]) if row[5] else {},
            enabled=row[6],
            created_at=row[7]
        )
    
    def list_workflows(self, enabled: Optional[bool] = None) -> List[WorkflowDefinition]:
        """List workflow definitions"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if enabled is not None:
            cursor.execute("""
                SELECT WORKFLOW_ID, NAME, DESCRIPTION, TRIGGER_CONDITION,
                       ACTION_TYPE, ACTION_CONFIG, ENABLED, CREATED_AT
                FROM WORKFLOW_DEFINITIONS
                WHERE ENABLED = %s
                ORDER BY CREATED_AT DESC
            """, (enabled,))
        else:
            cursor.execute("""
                SELECT WORKFLOW_ID, NAME, DESCRIPTION, TRIGGER_CONDITION,
                       ACTION_TYPE, ACTION_CONFIG, ENABLED, CREATED_AT
                FROM WORKFLOW_DEFINITIONS
                ORDER BY CREATED_AT DESC
            """)
        
        rows = cursor.fetchall()
        cursor.close()
        
        return [
            WorkflowDefinition(
                workflow_id=row[0],
                name=row[1],
                description=row[2],
                trigger_condition=row[3],
                action_type=row[4],
                action_config=json.loads(row[5]) if row[5] else {},
                enabled=row[6],
                created_at=row[7]
            )
            for row in rows
        ]
    
    def execute_workflow(
        self,
        workflow_id: str,
        entity_id: str,
        input_data: Dict[str, Any]
    ) -> WorkflowExecution:
        """Execute a workflow"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        execution_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Get workflow definition
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Create execution record
        cursor.execute("""
            INSERT INTO WORKFLOW_EXECUTIONS (
                EXECUTION_ID, WORKFLOW_ID, ENTITY_ID, STATUS,
                INPUT_DATA, STARTED_AT
            ) VALUES (%s, %s, %s, %s, PARSE_JSON(%s), %s)
        """, (
            execution_id,
            workflow_id,
            entity_id,
            WorkflowStatus.IN_PROGRESS.value,
            json.dumps(input_data),
            now
        ))
        
        conn.commit()
        
        # Execute the workflow action
        try:
            output_data = self._execute_workflow_action(
                workflow, entity_id, input_data, cursor
            )
            
            # Update execution as completed
            cursor.execute("""
                UPDATE WORKFLOW_EXECUTIONS
                SET STATUS = %s,
                    OUTPUT_DATA = PARSE_JSON(%s),
                    COMPLETED_AT = %s
                WHERE EXECUTION_ID = %s
            """, (
                WorkflowStatus.COMPLETED.value,
                json.dumps(output_data),
                datetime.utcnow(),
                execution_id
            ))
            
            conn.commit()
            status = WorkflowStatus.COMPLETED
            error_message = None
            
        except Exception as e:
            # Update execution as failed
            error_message = str(e)
            cursor.execute("""
                UPDATE WORKFLOW_EXECUTIONS
                SET STATUS = %s,
                    ERROR_MESSAGE = %s,
                    COMPLETED_AT = %s
                WHERE EXECUTION_ID = %s
            """, (
                WorkflowStatus.FAILED.value,
                error_message,
                datetime.utcnow(),
                execution_id
            ))
            
            conn.commit()
            status = WorkflowStatus.FAILED
            output_data = None
        
        cursor.close()
        
        return WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            entity_id=entity_id,
            status=status,
            input_data=input_data,
            output_data=output_data,
            error_message=error_message,
            started_at=now,
            completed_at=datetime.utcnow()
        )
    
    def _execute_workflow_action(
        self,
        workflow: WorkflowDefinition,
        entity_id: str,
        input_data: Dict[str, Any],
        cursor
    ) -> Dict[str, Any]:
        """Execute the actual workflow action"""
        action_type = workflow.action_type.upper()
        
        if action_type == "SQL":
            # Execute SQL action
            sql = workflow.action_config.get("sql", "")
            cursor.execute(sql, (entity_id,))
            result = cursor.fetchall()
            return {"result": "SQL executed", "rows_affected": cursor.rowcount}
        
        elif action_type == "NOTIFICATION":
            # Log notification (in production, send actual notification)
            message = workflow.action_config.get("message", "")
            return {
                "result": "Notification sent",
                "message": message,
                "entity_id": entity_id
            }
        
        elif action_type == "PYTHON":
            # Execute Python code (simplified - in production, use Snowpark)
            return {
                "result": "Python action executed",
                "entity_id": entity_id,
                "input_data": input_data
            }
        
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    def list_executions(
        self,
        workflow_id: Optional[str] = None,
        entity_id: Optional[str] = None,
        limit: int = 100
    ) -> List[WorkflowExecution]:
        """List workflow executions"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT EXECUTION_ID, WORKFLOW_ID, ENTITY_ID, STATUS,
                   INPUT_DATA, OUTPUT_DATA, ERROR_MESSAGE,
                   STARTED_AT, COMPLETED_AT
            FROM WORKFLOW_EXECUTIONS
            WHERE 1=1
        """
        params = []
        
        if workflow_id:
            query += " AND WORKFLOW_ID = %s"
            params.append(workflow_id)
        
        if entity_id:
            query += " AND ENTITY_ID = %s"
            params.append(entity_id)
        
        query += " ORDER BY STARTED_AT DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        
        return [
            WorkflowExecution(
                execution_id=row[0],
                workflow_id=row[1],
                entity_id=row[2],
                status=WorkflowStatus(row[3]),
                input_data=json.loads(row[4]) if row[4] else {},
                output_data=json.loads(row[5]) if row[5] else None,
                error_message=row[6],
                started_at=row[7],
                completed_at=row[8]
            )
            for row in rows
        ]
    
    def get_entity_state(self, entity_id: str) -> Optional[EntityState]:
        """Get the current state of an entity"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ENTITY_ID, CURRENT_STATE, PREVIOUS_STATE, STATE_DATA, UPDATED_AT
            FROM ENTITY_STATES
            WHERE ENTITY_ID = %s
        """, (entity_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        return EntityState(
            entity_id=row[0],
            current_state=row[1],
            previous_state=row[2],
            state_data=json.loads(row[3]) if row[3] else {},
            updated_at=row[4]
        )
    
    def update_entity_state(
        self,
        entity_id: str,
        new_state: str,
        state_data: Dict[str, Any]
    ) -> EntityState:
        """Update the state of an entity and trigger workflows"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get current state
        current_state_obj = self.get_entity_state(entity_id)
        previous_state = current_state_obj.current_state if current_state_obj else None
        
        now = datetime.utcnow()
        
        # Update or insert state
        if current_state_obj:
            cursor.execute("""
                UPDATE ENTITY_STATES
                SET CURRENT_STATE = %s,
                    PREVIOUS_STATE = %s,
                    STATE_DATA = PARSE_JSON(%s),
                    UPDATED_AT = %s
                WHERE ENTITY_ID = %s
            """, (new_state, previous_state, json.dumps(state_data), now, entity_id))
        else:
            cursor.execute("""
                INSERT INTO ENTITY_STATES (
                    ENTITY_ID, CURRENT_STATE, PREVIOUS_STATE, STATE_DATA, UPDATED_AT
                ) VALUES (%s, %s, %s, PARSE_JSON(%s), %s)
            """, (entity_id, new_state, previous_state, json.dumps(state_data), now))
        
        conn.commit()
        
        # Check for workflows that should be triggered
        self._check_and_trigger_workflows(entity_id, new_state, previous_state, cursor)
        
        cursor.close()
        
        return EntityState(
            entity_id=entity_id,
            current_state=new_state,
            previous_state=previous_state,
            state_data=state_data,
            updated_at=now
        )
    
    def _check_and_trigger_workflows(
        self,
        entity_id: str,
        new_state: str,
        previous_state: Optional[str],
        cursor
    ):
        """Check if any workflows should be triggered by this state change"""
        # Get enabled workflows
        cursor.execute("""
            SELECT WORKFLOW_ID, TRIGGER_CONDITION
            FROM WORKFLOW_DEFINITIONS
            WHERE ENABLED = TRUE
        """)
        
        workflows = cursor.fetchall()
        
        for workflow_id, trigger_condition in workflows:
            # Simple trigger matching (in production, use more sophisticated logic)
            if new_state in trigger_condition or trigger_condition == "*":
                # Trigger workflow asynchronously (in production, use Snowflake Tasks)
                try:
                    self.execute_workflow(
                        workflow_id,
                        entity_id,
                        {"new_state": new_state, "previous_state": previous_state}
                    )
                except Exception as e:
                    # Log error but don't fail state update
                    print(f"Error triggering workflow {workflow_id}: {e}")
