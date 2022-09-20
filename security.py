from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt

from schema import users, database
from models import User


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = 'HS256'
    SECRET_KEY='0auFzYdG8EOOx0a4YEL9a19J0eW-I9z-7eWCaAJ-mO1cZkIDFaQQtHbPX0uXPqgEp_JajdKMZg8zFs05nxNEOg'
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise RequiresLoginException()
        except jwt.JWTError as e:
            raise RequiresLoginException()
        except Exception as e:
            raise RequiresLoginException()
            
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


    def create_access_token(self,
        subject: Union[str, Any], expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes= self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


    def get_hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)


    def verify_password(self, plain_password, hash_password):
        return self.pwd_context.verify(plain_password, hash_password)


    async def authenticate_user(self, username, password):
        try:
            user = User(email = username,
                password= password)  
            query = users.select().where(users.c.email == user.email)
            result =  await database.fetch_one(query)
            if result: 
                password_check = self.verify_password(user.password, result[2])
                return password_check
            else: 
                return False
        except:
            raise RequiresLoginException()            


class RequiresLoginException(Exception):
    pass