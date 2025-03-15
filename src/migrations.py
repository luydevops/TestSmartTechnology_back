from src.database import engine
from src.models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("⏳ Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
logger.info("✅ Tablas creadas con éxito.")
