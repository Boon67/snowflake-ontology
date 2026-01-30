-- Setup script for Snowflake SPCS (Snowpark Container Services)
-- This script creates all necessary SPCS infrastructure

-- Use current role (SYSADMIN should have sufficient privileges)
USE DATABASE ONTOLOGY_DB;
USE SCHEMA PUBLIC;

-- Create compute pool for running containers
CREATE COMPUTE POOL IF NOT EXISTS ONTOLOGY_COMPUTE_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 3600
  COMMENT = 'Compute pool for Ontology & Workflow Engine';

-- Create image repository
CREATE IMAGE REPOSITORY IF NOT EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_IMAGES
  COMMENT = 'Repository for ontology engine container images';

-- Show repository URL for docker push
SHOW IMAGE REPOSITORIES LIKE 'ONTOLOGY_IMAGES' IN SCHEMA ONTOLOGY_DB.PUBLIC;

-- Create stage for service specs
CREATE STAGE IF NOT EXISTS ONTOLOGY_DB.PUBLIC.ONTOLOGY_STAGE
  COMMENT = 'Stage for service specification files';

-- Display setup information
SELECT 'SPCS infrastructure setup completed!' as STATUS;
SELECT 'Next steps:' as INSTRUCTIONS,
       '1. Build and push Docker images using deploy.sh' as STEP_1,
       '2. Create services using the service spec files' as STEP_2,
       '3. Access the application via the service endpoints' as STEP_3;
