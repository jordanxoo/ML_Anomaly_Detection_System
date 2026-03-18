from fastapi import Depends, APIRouter, HTTPException,Request
from app.schemas.user import UserCreate
from sqlalchemy import select
from app.core.limiter import limiter
from app.models.user import User
from app.core.security import hash_password, verify_password,create_access_token
from app.core.database import get_db, AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()


@router.post("/register")
async def user_register(req: UserCreate,db: AsyncSession = Depends(get_db)):
    
    user = await db.execute(select(User).where(User.username == req.username))
    user_obj = user.scalar_one_or_none()

    if(user_obj is None):
        raise HTTPException(400,"User already exsists")
    
    hashed_password = hash_password(req.password)
    user_created = User(username = req.username, hashed_password = hashed_password, 
                        email = req.email)
    
    db.add(user_created)
    await db.commit()

    return user_created


@router.post("/login")
@limiter.limit("5/minute")
async def user_login(request: Request,form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    
    user_found = await db.execute(select(User).where(User.username == form.username))
    user_obj = user_found.scalar_one_or_none()
    if(user_obj is None):
        raise HTTPException(401,"User not found in DB")
    
    password_match = verify_password(form.password,user_obj.hashed_password)

    if not password_match:
        raise HTTPException(401, "Passwords dont' match")
    

    jwt = create_access_token({"sub": form.username})
    return {"access_token":jwt,"token_type":"bearer"}



