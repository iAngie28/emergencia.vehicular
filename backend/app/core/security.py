from passlib.context import CryptContext

# Configuramos el algoritmo bcrypt (el estándar de oro)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_hash_clave(password: str) -> str:
    return pwd_context.hash(password)

def verificar_clave(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)