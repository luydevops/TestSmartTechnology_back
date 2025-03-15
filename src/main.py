from fastapi import FastAPI
from src.routes import users, gateway  # Importa ambos routers

app = FastAPI()

# Registrar routers
app.include_router(users.router)      # Rutas del microservicio de usuarios (sin cambios)
app.include_router(gateway.router)    # Rutas del API Gateway (con autenticación mejorada)
