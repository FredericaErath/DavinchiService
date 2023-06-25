"""
Authority handler. Use jwt verification.
"""
from typing import Optional

from jose import jwt
from fastapi import HTTPException, Security, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_pwd_hash(self, pwd):
        return self.pwd_context.hash(pwd)

    def verify_pwd(self, plain_pwd, hashed_pwd):
        return self.pwd_context.verify(plain_pwd, hashed_pwd)

    def encode_token(self, user_id):
        """Generate jwt."""
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token: Optional[str] = Header("")):
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            return payload['sub']
        except (jwt.ExpiredSignatureError, jwt.JWTError):
            raise HTTPException(status_code=401, detail='Token Error')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
