from sqlalchemy.orm import Session
from src.models import User
from src.schemas import UserCreate
from passlib.context import CryptContext

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Devuelve el hash de la contraseña dada en texto plano."""
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate) -> User:
    """
    Crea un nuevo usuario, hasheando la contraseña antes de almacenarla en la base de datos.
    """
    hashed_password = hash_password(user.password)
    db_user = User(
        nombre=user.nombre,
        correo=user.correo,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """
    Devuelve una lista de usuarios con paginación.
    :rtype: object
    """
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Recupera un usuario por su correo electrónico.
    """
    return db.query(User).filter(User.correo == email).first()

def delete_user(db: Session, user_id: int) -> bool:
    """
    Elimina un usuario por su ID. Retorna True si se eliminó, False si no se encontró.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
