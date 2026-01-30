import snowflake.connector
from snowflake.snowpark import Session
from config import settings
from typing import Optional
import os


class SnowflakeConnection:
    """Manages Snowflake database connections"""
    
    def __init__(self):
        self._connection = None
        self._session = None
    
    def get_connection(self):
        """Get a Snowflake connector connection"""
        if self._connection is None or self._connection.is_closed():
            # Check if running in SPCS (service token available)
            if os.path.exists("/snowflake/session/token"):
                # Running in SPCS - use service token
                with open("/snowflake/session/token", "r") as f:
                    token = f.read().strip()
                
                # Get SPCS environment variables (set by Snowflake when executeAsCaller is enabled)
                snowflake_host = os.getenv("SNOWFLAKE_HOST")
                snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
                
                if not snowflake_host or not snowflake_account:
                    raise ValueError("SPCS environment variables SNOWFLAKE_HOST and SNOWFLAKE_ACCOUNT must be set")
                
                connection_params = {
                    "host": snowflake_host,
                    "account": snowflake_account,
                    "authenticator": "oauth",
                    "token": token,
                    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE") or settings.snowflake_warehouse or "COMPUTE_WH",
                    "database": os.getenv("SNOWFLAKE_DATABASE") or settings.snowflake_database or "ONTOLOGY_DB",
                    "schema": os.getenv("SNOWFLAKE_SCHEMA") or settings.snowflake_schema or "PUBLIC",
                }
            else:
                # Running locally - use username/password
                connection_params = {
                    "account": settings.snowflake_account or os.getenv("SNOWFLAKE_ACCOUNT"),
                    "user": settings.snowflake_user or os.getenv("SNOWFLAKE_USER"),
                    "password": settings.snowflake_password or os.getenv("SNOWFLAKE_PASSWORD"),
                    "warehouse": settings.snowflake_warehouse or os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
                    "database": settings.snowflake_database or os.getenv("SNOWFLAKE_DATABASE", "ONTOLOGY_DB"),
                    "schema": settings.snowflake_schema or os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
                }
            
            if settings.snowflake_role or os.getenv("SNOWFLAKE_ROLE"):
                connection_params["role"] = settings.snowflake_role or os.getenv("SNOWFLAKE_ROLE")
            
            self._connection = snowflake.connector.connect(**connection_params)
        
        return self._connection
    
    def get_session(self) -> Session:
        """Get a Snowpark session"""
        if self._session is None:
            # Check if running in SPCS (service token available)
            if os.path.exists("/snowflake/session/token"):
                # Running in SPCS - use service token
                with open("/snowflake/session/token", "r") as f:
                    token = f.read().strip()
                
                # Get SPCS environment variables (set by Snowflake when executeAsCaller is enabled)
                snowflake_host = os.getenv("SNOWFLAKE_HOST")
                snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
                
                if not snowflake_host or not snowflake_account:
                    raise ValueError("SPCS environment variables SNOWFLAKE_HOST and SNOWFLAKE_ACCOUNT must be set")
                
                connection_params = {
                    "host": snowflake_host,
                    "account": snowflake_account,
                    "authenticator": "oauth",
                    "token": token,
                    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE") or settings.snowflake_warehouse or "COMPUTE_WH",
                    "database": os.getenv("SNOWFLAKE_DATABASE") or settings.snowflake_database or "ONTOLOGY_DB",
                    "schema": os.getenv("SNOWFLAKE_SCHEMA") or settings.snowflake_schema or "PUBLIC",
                }
            else:
                # Running locally - use username/password
                connection_params = {
                    "account": settings.snowflake_account or os.getenv("SNOWFLAKE_ACCOUNT"),
                    "user": settings.snowflake_user or os.getenv("SNOWFLAKE_USER"),
                    "password": settings.snowflake_password or os.getenv("SNOWFLAKE_PASSWORD"),
                    "warehouse": settings.snowflake_warehouse or os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
                    "database": settings.snowflake_database or os.getenv("SNOWFLAKE_DATABASE", "ONTOLOGY_DB"),
                    "schema": settings.snowflake_schema or os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
                }
            
            if settings.snowflake_role or os.getenv("SNOWFLAKE_ROLE"):
                connection_params["role"] = settings.snowflake_role or os.getenv("SNOWFLAKE_ROLE")
            
            self._session = Session.builder.configs(connection_params).create()
        
        return self._session
    
    def close(self):
        """Close all connections"""
        if self._connection and not self._connection.is_closed():
            self._connection.close()
        if self._session:
            self._session.close()


# Global connection instance
db = SnowflakeConnection()
