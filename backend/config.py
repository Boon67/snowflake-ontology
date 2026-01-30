from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Snowflake connection settings
    snowflake_account: str = ""
    snowflake_user: str = ""
    snowflake_password: str = ""
    snowflake_warehouse: str = "COMPUTE_WH"
    snowflake_database: str = "ONTOLOGY_DB"
    snowflake_schema: str = "PUBLIC"
    snowflake_role: Optional[str] = None
    
    # Application settings
    app_name: str = "Snowflake Ontology & Workflow Engine"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
