import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
import os
load_dotenv()


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("JWT_KEY", "aVeryComplexSecretKey")

    def get_password_hash(self, password):
        print("get_password_hash")
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user):
        payload = {
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=1, minutes=0),
            'iat': datetime.now(tz=timezone.utc),
            "id": str(user.id),
            "email": user.email
        }
        print(self.secret)
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        print("Decoding token")
        print(token)
        try:
            print(self.secret)
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            print(payload)
            return {
                "id": payload['id'],
                "email": payload['email']
            }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
