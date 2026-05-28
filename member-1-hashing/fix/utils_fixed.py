from datetime import datetime, timedelta, timezone
from typing import Union
import os
import re
import time
import secrets
from fastapi import HTTPException
from apis.auth.exceptions import UserAlreadyExistsException
from config import Settings
from db.models import User, UserRole
from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

#cubre: API2:2023, A02:2021, A07:2021
#broken authenticaction | fallos de criptografía | fallos de auth
SECRET_KEY = Settings.JWT_SECRET_KEY
ALGORITHM = "HS256"

#hardening: personalizar los parametros que ofrece argo2 para mayor seguridad ante ataques
ph = PasswordHasher(
    time_cost=3, 
    memory_cost=65536, 
    parallelism=4, 
    hash_len=32, 
    salt_len=16
)

# Hash precalculado para mitigar ataques de tiempo (Timing Attacks)
DUMMY_HASH = ph.hash(secrets.token_urlsafe(16))

def validate_password_strength(password: str):
    #uso de regex para validación de contraseñas (criterios de longitud, May/Min, numeros, simbolos)
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")

def verify_password(plain_password, hashed_password):
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False

def get_password_hash(password):
    return ph.hash(password)

def get_user_by_username(db, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    
    if not user:
        # TIMING ATTACK:
        # Si el usuario no existe, se aplica un hash igual para que el servidor
        # tarde el mismo tiempo en responder y el time response sea constante
        try:
            ph.verify(DUMMY_HASH, password)
        except:
            pass
        return False
        
    if not verify_password(password, user.password):
        # FUERZA BRUTA (Tarpitting):
        # delay de x tiempo para contraseñas incorrectas y evitar fuerza bruta
        time.sleep(0.5)
        return False
        
    return user

def create_user(db, username, password, first_name, last_name, phone_number, role=UserRole.CUSTOMER):
    if get_user_by_username(db, username):
        raise UserAlreadyExistsException()
        
    # validar el hash antes de procesar (crterios)
    validate_password_strength(password)
    
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user_password(db, username: str, password: str) -> User:
    validate_password_strength(password)
    db_user = get_user_by_username(db, username)
    db_user.password = get_password_hash(password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_phone_number(db, phone_number: str) -> User:
    return db.query(User).filter(User.phone_number == phone_number).first()

def create_user_if_not_exists(db, username, password, first_name, last_name, phone_number, role=UserRole.CUSTOMER):
    try:
        return create_user(db, username, password, first_name, last_name, phone_number, role)
    except UserAlreadyExistsException:
        return None

def update_user(db, username: str, user):
    db_user = get_user_by_username(db, username)
    for var, value in vars(user).items():
        if value:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def send_code_to_phone_number(phone_number: str, code: str):
    print(f"Sending code {code} to phone number {phone_number}")
    return True
