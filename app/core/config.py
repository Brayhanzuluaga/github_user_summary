from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "GitHub User Summary API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    github_api_base_url: str = "https://api.github.com"
    github_api_version: str = "2022-11-28"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

