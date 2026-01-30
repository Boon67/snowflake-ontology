-- Snowflake Ontology & Workflow Engine Database Setup
-- This script creates all necessary database objects

-- Create database and schema
CREATE DATABASE IF NOT EXISTS ONTOLOGY_DB;
USE DATABASE ONTOLOGY_DB;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- ==================== ENTITIES TABLE ====================
-- Stores all entities in the ontology
CREATE TABLE IF NOT EXISTS ENTITIES (
    ENTITY_ID VARCHAR(36) PRIMARY KEY,
    ENTITY_TYPE VARCHAR(100) NOT NULL,
    LABEL VARCHAR(500) NOT NULL,
    PROPERTIES VARIANT,
    TAGS VARIANT,
    CREATED_AT TIMESTAMP_NTZ NOT NULL,
    UPDATED_AT TIMESTAMP_NTZ NOT NULL
);

-- Note: Indexes are not supported on standard tables in Snowflake
-- Clustering keys can be used instead for large tables

-- ==================== RELATIONSHIPS TABLE ====================
-- Stores relationships between entities (Subject -> Predicate -> Object)
CREATE TABLE IF NOT EXISTS RELATIONSHIPS (
    RELATIONSHIP_ID VARCHAR(36) PRIMARY KEY,
    SUBJECT_ID VARCHAR(36) NOT NULL,
    PREDICATE VARCHAR(200) NOT NULL,
    OBJECT_ID VARCHAR(36) NOT NULL,
    PROPERTIES VARIANT,
    CREATED_AT TIMESTAMP_NTZ NOT NULL,
    FOREIGN KEY (SUBJECT_ID) REFERENCES ENTITIES(ENTITY_ID),
    FOREIGN KEY (OBJECT_ID) REFERENCES ENTITIES(ENTITY_ID)
);

-- Note: Indexes are not supported on standard tables in Snowflake

-- ==================== ENTITY STATES TABLE ====================
-- Tracks the current state of each entity for workflow management
CREATE TABLE IF NOT EXISTS ENTITY_STATES (
    ENTITY_ID VARCHAR(36) PRIMARY KEY,
    CURRENT_STATE VARCHAR(100) NOT NULL,
    PREVIOUS_STATE VARCHAR(100),
    STATE_DATA VARIANT,
    UPDATED_AT TIMESTAMP_NTZ NOT NULL,
    FOREIGN KEY (ENTITY_ID) REFERENCES ENTITIES(ENTITY_ID)
);

-- Note: Indexes are not supported on standard tables in Snowflake

-- ==================== WORKFLOW DEFINITIONS TABLE ====================
-- Defines workflows that can be triggered by state changes
CREATE TABLE IF NOT EXISTS WORKFLOW_DEFINITIONS (
    WORKFLOW_ID VARCHAR(36) PRIMARY KEY,
    NAME VARCHAR(200) NOT NULL,
    DESCRIPTION TEXT,
    TRIGGER_CONDITION VARCHAR(500) NOT NULL,
    ACTION_TYPE VARCHAR(50) NOT NULL,
    ACTION_CONFIG VARIANT NOT NULL,
    ENABLED BOOLEAN DEFAULT TRUE,
    CREATED_AT TIMESTAMP_NTZ NOT NULL
);

-- Note: Indexes are not supported on standard tables in Snowflake

-- ==================== WORKFLOW EXECUTIONS TABLE ====================
-- Tracks execution history of workflows
CREATE TABLE IF NOT EXISTS WORKFLOW_EXECUTIONS (
    EXECUTION_ID VARCHAR(36) PRIMARY KEY,
    WORKFLOW_ID VARCHAR(36) NOT NULL,
    ENTITY_ID VARCHAR(36) NOT NULL,
    STATUS VARCHAR(50) NOT NULL,
    INPUT_DATA VARIANT,
    OUTPUT_DATA VARIANT,
    ERROR_MESSAGE TEXT,
    STARTED_AT TIMESTAMP_NTZ NOT NULL,
    COMPLETED_AT TIMESTAMP_NTZ,
    FOREIGN KEY (WORKFLOW_ID) REFERENCES WORKFLOW_DEFINITIONS(WORKFLOW_ID),
    FOREIGN KEY (ENTITY_ID) REFERENCES ENTITIES(ENTITY_ID)
);

-- Note: Indexes are not supported on standard tables in Snowflake

-- ==================== STREAMS FOR CDC ====================
-- Create streams to capture changes for workflow triggers

-- Stream for entity changes
CREATE STREAM IF NOT EXISTS ENTITIES_STREAM ON TABLE ENTITIES;

-- Stream for state changes
CREATE STREAM IF NOT EXISTS ENTITY_STATES_STREAM ON TABLE ENTITY_STATES;

-- ==================== DYNAMIC TABLES ====================
-- Automatically materialized views for complex queries

-- Entity relationship summary
CREATE OR REPLACE DYNAMIC TABLE ENTITY_RELATIONSHIP_SUMMARY
    TARGET_LAG = '1 minute'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    e.ENTITY_ID,
    e.ENTITY_TYPE,
    e.LABEL,
    COUNT(DISTINCT r1.RELATIONSHIP_ID) as OUTGOING_RELATIONSHIPS,
    COUNT(DISTINCT r2.RELATIONSHIP_ID) as INCOMING_RELATIONSHIPS,
    e.UPDATED_AT
FROM ENTITIES e
LEFT JOIN RELATIONSHIPS r1 ON e.ENTITY_ID = r1.SUBJECT_ID
LEFT JOIN RELATIONSHIPS r2 ON e.ENTITY_ID = r2.OBJECT_ID
GROUP BY e.ENTITY_ID, e.ENTITY_TYPE, e.LABEL, e.UPDATED_AT;

-- Workflow execution summary
CREATE OR REPLACE DYNAMIC TABLE WORKFLOW_EXECUTION_SUMMARY
    TARGET_LAG = '5 minutes'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    w.WORKFLOW_ID,
    w.NAME,
    COUNT(CASE WHEN e.STATUS = 'COMPLETED' THEN 1 END) as COMPLETED_COUNT,
    COUNT(CASE WHEN e.STATUS = 'FAILED' THEN 1 END) as FAILED_COUNT,
    COUNT(CASE WHEN e.STATUS = 'IN_PROGRESS' THEN 1 END) as IN_PROGRESS_COUNT,
    MAX(e.STARTED_AT) as LAST_EXECUTION
FROM WORKFLOW_DEFINITIONS w
LEFT JOIN WORKFLOW_EXECUTIONS e ON w.WORKFLOW_ID = e.WORKFLOW_ID
GROUP BY w.WORKFLOW_ID, w.NAME;

-- ==================== TASKS FOR WORKFLOW AUTOMATION ====================
-- Note: Complex tasks with stored procedure logic can be added later
-- For now, workflows can be triggered via API or scheduled tasks

-- ==================== STORED PROCEDURES ====================
-- Useful procedures for ontology operations

-- Procedure to get entity with all relationships
CREATE OR REPLACE PROCEDURE GET_ENTITY_WITH_RELATIONSHIPS(ENTITY_ID_PARAM VARCHAR)
RETURNS TABLE (ENTITY_ID VARCHAR, ENTITY_TYPE VARCHAR, LABEL VARCHAR, RELATIONSHIP_TYPE VARCHAR, RELATED_ENTITY_ID VARCHAR, RELATED_LABEL VARCHAR)
LANGUAGE SQL
AS
$$
BEGIN
    LET result_set RESULTSET := (
        SELECT 
            e.ENTITY_ID,
            e.ENTITY_TYPE,
            e.LABEL,
            'OUTGOING' as RELATIONSHIP_TYPE,
            r.OBJECT_ID as RELATED_ENTITY_ID,
            e2.LABEL as RELATED_LABEL
        FROM ENTITIES e
        JOIN RELATIONSHIPS r ON e.ENTITY_ID = r.SUBJECT_ID
        JOIN ENTITIES e2 ON r.OBJECT_ID = e2.ENTITY_ID
        WHERE e.ENTITY_ID = :ENTITY_ID_PARAM
        
        UNION ALL
        
        SELECT 
            e.ENTITY_ID,
            e.ENTITY_TYPE,
            e.LABEL,
            'INCOMING' as RELATIONSHIP_TYPE,
            r.SUBJECT_ID as RELATED_ENTITY_ID,
            e2.LABEL as RELATED_LABEL
        FROM ENTITIES e
        JOIN RELATIONSHIPS r ON e.ENTITY_ID = r.OBJECT_ID
        JOIN ENTITIES e2 ON r.SUBJECT_ID = e2.ENTITY_ID
        WHERE e.ENTITY_ID = :ENTITY_ID_PARAM
    );
    RETURN TABLE(result_set);
END;
$$;

-- ==================== SAMPLE DATA ====================
-- Note: Sample data insertion skipped to avoid conflicts
-- Data can be added via the API or manually

-- ==================== VIEWS ====================
-- Useful views for querying the ontology

-- View: Entity graph with relationships
CREATE OR REPLACE VIEW V_ENTITY_GRAPH AS
SELECT 
    e1.ENTITY_ID as SOURCE_ID,
    e1.ENTITY_TYPE as SOURCE_TYPE,
    e1.LABEL as SOURCE_LABEL,
    r.PREDICATE,
    e2.ENTITY_ID as TARGET_ID,
    e2.ENTITY_TYPE as TARGET_TYPE,
    e2.LABEL as TARGET_LABEL,
    r.PROPERTIES as RELATIONSHIP_PROPERTIES
FROM RELATIONSHIPS r
JOIN ENTITIES e1 ON r.SUBJECT_ID = e1.ENTITY_ID
JOIN ENTITIES e2 ON r.OBJECT_ID = e2.ENTITY_ID;

-- View: Entity with current state
CREATE OR REPLACE VIEW V_ENTITIES_WITH_STATE AS
SELECT 
    e.*,
    s.CURRENT_STATE,
    s.PREVIOUS_STATE,
    s.STATE_DATA
FROM ENTITIES e
LEFT JOIN ENTITY_STATES s ON e.ENTITY_ID = s.ENTITY_ID;

-- Grant necessary permissions (adjust as needed)
GRANT USAGE ON DATABASE ONTOLOGY_DB TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA PUBLIC TO ROLE PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA PUBLIC TO ROLE PUBLIC;
GRANT SELECT ON ALL VIEWS IN SCHEMA PUBLIC TO ROLE PUBLIC;
GRANT USAGE ON ALL PROCEDURES IN SCHEMA PUBLIC TO ROLE PUBLIC;

-- Display setup completion message
SELECT 'Snowflake Ontology & Workflow Engine database setup completed successfully!' as STATUS;
