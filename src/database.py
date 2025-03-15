from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings  # Usamos la instancia global de Settings

# Construir la URL de conexión a PostgreSQL utilizando settings
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
)

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Genera una sesión de base de datos para ser usada en las dependencias."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db():
    """Prueba la conexión a la base de datos."""
    try:
        connection = engine.connect()
        print("✅ Conexión a PostgreSQL exitosa")
        connection.close()
    except Exception as e:
        print(f"❌ Error al conectar con PostgreSQL: {e}")
