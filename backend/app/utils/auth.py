from passlib.context import CryptContext  # its like saying passlib that i want to use bcrypt for pswd hashing
from jose import jwt
from datetime import datetime, timedelta
import os  # to read env var

from fastapi import Depends, HTTPException
from app.database import get_db
from app import models, schemas

from fastapi.security import OAuth2PasswordBearer # it is basically a JWT/token extractor for FastAPI.
from sqlalchemy.orm import Session
from jose import JWTError

# configuring pswd hashing 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #-->  
#                         telling passlib to use 
#                         the hashing algo


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"    # --> This tells python-jose: Use HS256 to create/verify the JWT signature.,HS256 is the algorithm used to create and verify the JWT signature.
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24    # AFTER 1 DAY TOKEN WILL EXPIRE


# takes a plain text pswd and returns its bcrypt hash
def hash_password(password:str) -> str: # expected to return a string ,  # pswd hashing using bcrypt 
    return pwd_context.hash(password)


# checks if the entered pswd matches the stored bcrypt hash nd returns true/false
def verify_password(plain_password:str, hashed_password:str) -> bool:  # to verify user pswd 
    return pwd_context.verify(plain_password, hashed_password)

# takes user info, adds expiration time nd creates a signed jwt using SECRET_KEY + HS256
def create_access_token(data:dict) -> str:  # takes user info and convert it into jwt 
    to_encode = data.copy()  #  copy the user data 
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # cur time + 24 hr --> expiration time 
    to_encode.update({"exp":expire}) # we add expiration time to that copied data 

# now jwt knows user data , and expiration time 

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # jwt created using to_encode,secret_key nd the algo

# user data + SECRET_KEY -> HS256 -> JWT signature


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # creates the token extraction dependency , it tells fastapi that thi is the endpt where client get a token it /auth/login 
# jwt has header + payload + secret key + HS256 --> signature 


# extracts nd verifies jwt, gets user email from sub, finds that user in postgresql, nd return user obj 
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):  # cheks if a request contains a JWT. Who is this user, and is the JWT valid? etc 
                  # it tells fastapi ,run oauth2scheme, extract the token from request, nd give it to me as token
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},) # creating error to use it later 

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # for jwt verification 
        email = payload.get("sub")  # taking the value stored under sub which is user.email
        if email is None:   
            raise credentials_exception
    
    except JWTError:  # if jwt not matched then error 
        raise credentials_exception
    

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user