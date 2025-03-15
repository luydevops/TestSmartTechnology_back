from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from jose import JWTError, jwt
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.models import Token
from src.database import get_db
from src.schemas import UserResponse
from src import crud, schemas


# Cargar variables de entorno
load_dotenv()

# Clave secreta para firmar los tokens
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

# Configurar el esquema de autenticación usando OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(user_id: int, db: Session, expires_delta: Optional[timedelta] = None):
    """Genera y almacena un token JWT en la base de datos."""
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Guardar en la base de datos
    db_token = Token(user_id=user_id, token=token, expires_at=expire)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token

def remove_token_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    """
    Elimina el token de la base de datos, invalidándolo.
    """
    db_token = db.query(Token).filter(Token.token == token).first()
    if db_token:
        db.delete(db_token)
        db.commit()
    return {"message": "Token eliminado correctamente."}


def verify_token(token: str, db: Session):
    """Verifica si el token es válido y está activo en la base de datos."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        # Buscar el token en la base de datos
        db_token = db.query(Token).filter(Token.token == token).first()
        if not db_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o revocado")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    """Extrae el usuario desde el token JWT y obtiene su información desde la base de datos."""
    payload = verify_token(token, db)
    user_id = int(payload.get("sub"))

    # Obtener el usuario de la base de datos
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    # Convertimos el modelo de la base de datos a UserResponse
    return schemas.UserResponse(**user.__dict__)



def get_current_valid_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
) -> schemas.UserResponse:
    """Verifica el usuario autenticado y que no esté deshabilitado."""
    user = get_current_user(token, db)  # Usa la función existente para obtener el usuario

    if user.disabled:  # Si está deshabilitado, bloqueamos el acceso
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

    return user  # Devuelve el usuario si está activo
