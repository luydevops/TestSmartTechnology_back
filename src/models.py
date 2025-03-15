from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from passlib.context import CryptContext
from datetime import datetime, timedelta

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=True)  # <-- Este campo debe existir

    def verify_password(self, plain_password: str) -> bool:
        """Verifica si la contraseña en texto plano coincide con el hash almacenado."""
        return pwd_context.verify(plain_password, self.password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Retorna el hash de una contraseña en texto plano."""
        return pwd_context.hash(plain_password)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, correo={self.correo})>"

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", backref="tokens")

    def __repr__(self) -> str:
        return f"<Token(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"
