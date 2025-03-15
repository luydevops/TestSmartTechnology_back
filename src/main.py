from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import users, gateway  # Importa ambos routers

app = FastAPI()

# Configuración de CORS
origins = [
    "http://192.168.0.105:3000",
    "http://localhost:8010",
    "http://localhost:3010",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(users.router)  # Rutas del microservicio de usuarios (sin cambios)
app.include_router(gateway.router)  # Rutas del API Gateway (con autenticación mejorada)
