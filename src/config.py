from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432  # Valor por defecto: 5432
    PROJECT_NAME: str = "TestSmarTe API"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "supersecreto"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"  # Carga automáticamente las variables de entorno desde .env

# Instancia global de configuración
settings = Settings()

