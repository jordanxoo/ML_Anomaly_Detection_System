from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings
from datetime import timedelta,timezone,datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException


context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") 


def hash_password(password : str) -> str:

    if(password != None):
        hashed = context.hash(password)
        return hashed
    else:
        return "No password provided"
    

def verify_password(plain: str, hashed: str) -> bool:

    return context.verify(plain,hash=hashed)

def create_access_token(data: dict) -> str:
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data['exp'] = expire
    token = jwt.encode(data,settings.SECRET_KEY,algorithm="HS256")

    return token

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:   
        jwt_token = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
    except JWTError:
        raise HTTPException(401, "Invalid token")
    
    username = jwt_token["sub"]
    if username == None:
        raise HTTPException(401,"Username not found")
    
    return username