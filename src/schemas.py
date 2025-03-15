from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Esquema para la creación de un usuario (entrada)
class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str  # Se espera la contraseña en el input

# Esquema para la respuesta de un usuario (salida)
class UserResponse(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    disabled: bool  # Agregamos este campo

    class Config:
        orm_mode = True  # Permite convertir modelos de SQLAlchemy a Pydantic

# Esquema para el login de un usuario
class UserLogin(BaseModel):
    correo: EmailStr
    password: str

# Esquema para la respuesta del token
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para los datos del token (útil para validación interna)
class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []
