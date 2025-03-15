from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src import crud, schemas
from src.auth import create_access_token, get_current_user, remove_token_user



router = APIRouter(prefix="/gateway", tags=["gateway"])

# Login para generar el token
@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_credentials.correo)
    if not user or not user.verify_password(user_credentials.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    # Corrección: Usar el ID del usuario en lugar del correo
    access_token = create_access_token(user_id=user.id, db=db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(response: dict = Depends(remove_token_user)):
    """
    Cierra sesión eliminando el token de la base de datos.
    """
    return response



@router.get("/users/", response_model=list[schemas.UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token_data: dict = Depends(get_current_user)):
    data=''
    if(token_data):
        data = crud.get_users(db, skip=skip, limit=limit)
    return data

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(get_current_user)  # Requiere autenticación
):
    """Crea un nuevo usuario en la base de datos si el token es válido."""
    data = None
    if token_data:
        data = crud.create_user(db, user)
    return data


