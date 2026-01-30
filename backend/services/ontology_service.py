import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from database import SnowflakeConnection
from models import Entity, EntityResponse, Relationship, RelationshipResponse, GraphQuery


class OntologyService:
    """Service for managing ontology entities and relationships"""
    
    def __init__(self, db: SnowflakeConnection):
        self.db = db
    
    def create_entity(self, entity: Entity) -> EntityResponse:
        """Create a new entity in the ontology"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        entity_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        cursor.execute("""
            INSERT INTO ENTITIES (
                ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT
            ) VALUES (%s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), %s, %s)
        """, (
            entity_id,
            entity.entity_type,
            entity.label,
            json.dumps(entity.properties),
            json.dumps(entity.tags),
            now,
            now
        ))
        
        conn.commit()
        cursor.close()
        
        return EntityResponse(
            entity_id=entity_id,
            entity_type=entity.entity_type,
            label=entity.label,
            properties=entity.properties,
            tags=entity.tags,
            created_at=now,
            updated_at=now
        )
    
    def get_entity(self, entity_id: str) -> Optional[EntityResponse]:
        """Get an entity by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT
            FROM ENTITIES
            WHERE ENTITY_ID = %s
        """, (entity_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        return EntityResponse(
            entity_id=row[0],
            entity_type=row[1],
            label=row[2],
            properties=json.loads(row[3]) if row[3] else {},
            tags=json.loads(row[4]) if row[4] else [],
            created_at=row[5],
            updated_at=row[6]
        )
    
    def list_entities(
        self,
        entity_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EntityResponse]:
        """List entities with optional filtering"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if entity_type:
            cursor.execute("""
                SELECT ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT
                FROM ENTITIES
                WHERE ENTITY_TYPE = %s
                ORDER BY CREATED_AT DESC
                LIMIT %s OFFSET %s
            """, (entity_type, limit, offset))
        else:
            cursor.execute("""
                SELECT ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT
                FROM ENTITIES
                ORDER BY CREATED_AT DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
        
        rows = cursor.fetchall()
        cursor.close()
        
        return [
            EntityResponse(
                entity_id=row[0],
                entity_type=row[1],
                label=row[2],
                properties=json.loads(row[3]) if row[3] else {},
                tags=json.loads(row[4]) if row[4] else [],
                created_at=row[5],
                updated_at=row[6]
            )
            for row in rows
        ]
    
    def update_entity(self, entity_id: str, entity: Entity) -> Optional[EntityResponse]:
        """Update an existing entity"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        now = datetime.utcnow()
        
        cursor.execute("""
            UPDATE ENTITIES
            SET ENTITY_TYPE = %s,
                LABEL = %s,
                PROPERTIES = PARSE_JSON(%s),
                TAGS = PARSE_JSON(%s),
                UPDATED_AT = %s
            WHERE ENTITY_ID = %s
        """, (
            entity.entity_type,
            entity.label,
            json.dumps(entity.properties),
            json.dumps(entity.tags),
            now,
            entity_id
        ))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            return None
        
        cursor.close()
        return self.get_entity(entity_id)
    
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Delete related relationships first
        cursor.execute("""
            DELETE FROM RELATIONSHIPS
            WHERE SUBJECT_ID = %s OR OBJECT_ID = %s
        """, (entity_id, entity_id))
        
        # Delete the entity
        cursor.execute("""
            DELETE FROM ENTITIES
            WHERE ENTITY_ID = %s
        """, (entity_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        
        return success
    
    def create_relationship(self, relationship: Relationship) -> RelationshipResponse:
        """Create a new relationship between entities"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        relationship_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        cursor.execute("""
            INSERT INTO RELATIONSHIPS (
                RELATIONSHIP_ID, SUBJECT_ID, PREDICATE, OBJECT_ID, PROPERTIES, CREATED_AT
            ) VALUES (%s, %s, %s, %s, PARSE_JSON(%s), %s)
        """, (
            relationship_id,
            relationship.subject_id,
            relationship.predicate,
            relationship.object_id,
            json.dumps(relationship.properties),
            now
        ))
        
        conn.commit()
        cursor.close()
        
        return RelationshipResponse(
            relationship_id=relationship_id,
            subject_id=relationship.subject_id,
            predicate=relationship.predicate,
            object_id=relationship.object_id,
            properties=relationship.properties,
            created_at=now
        )
    
    def list_relationships(
        self,
        entity_id: Optional[str] = None,
        predicate: Optional[str] = None,
        limit: int = 100
    ) -> List[RelationshipResponse]:
        """List relationships with optional filtering"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT RELATIONSHIP_ID, SUBJECT_ID, PREDICATE, OBJECT_ID, PROPERTIES, CREATED_AT
            FROM RELATIONSHIPS
            WHERE 1=1
        """
        params = []
        
        if entity_id:
            query += " AND (SUBJECT_ID = %s OR OBJECT_ID = %s)"
            params.extend([entity_id, entity_id])
        
        if predicate:
            query += " AND PREDICATE = %s"
            params.append(predicate)
        
        query += " ORDER BY CREATED_AT DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        
        return [
            RelationshipResponse(
                relationship_id=row[0],
                subject_id=row[1],
                predicate=row[2],
                object_id=row[3],
                properties=json.loads(row[4]) if row[4] else {},
                created_at=row[5]
            )
            for row in rows
        ]
    
    def delete_relationship(self, relationship_id: str) -> bool:
        """Delete a relationship"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM RELATIONSHIPS
            WHERE RELATIONSHIP_ID = %s
        """, (relationship_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        
        return success
    
    def query_graph(self, query: GraphQuery) -> Dict[str, Any]:
        """Query the ontology graph using iterative traversal (Snowflake compatible)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Simplified approach: Get entities within N hops
        # Start with the initial entity
        visited_entities = set()
        all_nodes = []
        all_edges = []
        
        # Get start entity
        cursor.execute("""
            SELECT ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES
            FROM ENTITIES
            WHERE ENTITY_ID = %s
        """, (query.start_entity_id,))
        
        start_row = cursor.fetchone()
        if not start_row:
            cursor.close()
            return {"nodes": [], "edges": [], "total_nodes": 0, "total_edges": 0}
        
        all_nodes.append({
            "entity_id": start_row[0],
            "entity_type": start_row[1],
            "label": start_row[2],
            "properties": json.loads(start_row[3]) if start_row[3] else {},
            "depth": 0
        })
        visited_entities.add(start_row[0])
        
        # Iteratively find connected entities up to max_depth
        current_level = [start_row[0]]
        
        for depth in range(1, query.max_depth + 1):
            if not current_level:
                break
            
            next_level = []
            placeholders = ", ".join(["%s"] * len(current_level))
            
            # Build query based on direction
            if query.direction == "outgoing":
                rel_query = f"""
                    SELECT DISTINCT
                        r.RELATIONSHIP_ID,
                        r.SUBJECT_ID,
                        r.PREDICATE,
                        r.OBJECT_ID,
                        r.PROPERTIES,
                        e.ENTITY_TYPE,
                        e.LABEL,
                        e.PROPERTIES as ENTITY_PROPERTIES
                    FROM RELATIONSHIPS r
                    JOIN ENTITIES e ON r.OBJECT_ID = e.ENTITY_ID
                    WHERE r.SUBJECT_ID IN ({placeholders})
                """
            elif query.direction == "incoming":
                rel_query = f"""
                    SELECT DISTINCT
                        r.RELATIONSHIP_ID,
                        r.SUBJECT_ID,
                        r.PREDICATE,
                        r.OBJECT_ID,
                        r.PROPERTIES,
                        e.ENTITY_TYPE,
                        e.LABEL,
                        e.PROPERTIES as ENTITY_PROPERTIES
                    FROM RELATIONSHIPS r
                    JOIN ENTITIES e ON r.SUBJECT_ID = e.ENTITY_ID
                    WHERE r.OBJECT_ID IN ({placeholders})
                """
            else:  # both
                rel_query = f"""
                    SELECT DISTINCT
                        r.RELATIONSHIP_ID,
                        r.SUBJECT_ID,
                        r.PREDICATE,
                        r.OBJECT_ID,
                        r.PROPERTIES,
                        e.ENTITY_TYPE,
                        e.LABEL,
                        e.PROPERTIES as ENTITY_PROPERTIES
                    FROM RELATIONSHIPS r
                    JOIN ENTITIES e ON (
                        (r.SUBJECT_ID IN ({placeholders}) AND e.ENTITY_ID = r.OBJECT_ID)
                        OR (r.OBJECT_ID IN ({placeholders}) AND e.ENTITY_ID = r.SUBJECT_ID)
                    )
                    WHERE r.SUBJECT_ID IN ({placeholders}) OR r.OBJECT_ID IN ({placeholders})
                """
            
            # Execute query
            if query.direction == "both":
                params = current_level * 4
            else:
                params = current_level
            
            cursor.execute(rel_query, params)
            rows = cursor.fetchall()
            
            for row in rows:
                rel_id, subj_id, pred, obj_id, rel_props, ent_type, ent_label, ent_props = row
                
                # Add edge
                edge = {
                    "relationship_id": rel_id,
                    "subject_id": subj_id,
                    "predicate": pred,
                    "object_id": obj_id,
                    "properties": json.loads(rel_props) if rel_props else {}
                }
                if edge not in all_edges:
                    all_edges.append(edge)
                
                # Determine the new entity based on direction
                if query.direction == "outgoing":
                    new_entity_id = obj_id
                elif query.direction == "incoming":
                    new_entity_id = subj_id
                else:  # both
                    # Find which one is new
                    if subj_id in current_level and obj_id not in visited_entities:
                        new_entity_id = obj_id
                    elif obj_id in current_level and subj_id not in visited_entities:
                        new_entity_id = subj_id
                    else:
                        continue
                
                # Add node if not visited
                if new_entity_id not in visited_entities:
                    all_nodes.append({
                        "entity_id": new_entity_id,
                        "entity_type": ent_type,
                        "label": ent_label,
                        "properties": json.loads(ent_props) if ent_props else {},
                        "depth": depth
                    })
                    visited_entities.add(new_entity_id)
                    next_level.append(new_entity_id)
            
            current_level = next_level
        
        cursor.close()
        
        return {
            "nodes": all_nodes,
            "edges": all_edges,
            "total_nodes": len(all_nodes),
            "total_edges": len(all_edges)
        }
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Get statistics about the ontology graph"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get entity counts by type
        cursor.execute("""
            SELECT ENTITY_TYPE, COUNT(*) as COUNT
            FROM ENTITIES
            GROUP BY ENTITY_TYPE
            ORDER BY COUNT DESC
        """)
        entity_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Get total entities
        cursor.execute("SELECT COUNT(*) FROM ENTITIES")
        total_entities = cursor.fetchone()[0]
        
        # Get relationship counts by predicate
        cursor.execute("""
            SELECT PREDICATE, COUNT(*) as COUNT
            FROM RELATIONSHIPS
            GROUP BY PREDICATE
            ORDER BY COUNT DESC
        """)
        relationship_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Get total relationships
        cursor.execute("SELECT COUNT(*) FROM RELATIONSHIPS")
        total_relationships = cursor.fetchone()[0]
        
        cursor.close()
        
        return {
            "total_entities": total_entities,
            "total_relationships": total_relationships,
            "entities_by_type": entity_counts,
            "relationships_by_predicate": relationship_counts
        }
