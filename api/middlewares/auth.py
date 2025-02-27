import jwt
import bcrypt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
import os
load_dotenv()

class AuthHandler():
    security = HTTPBearer()
    secret = os.getenv("JWT_KEY", "aVeryComplexSecretKey")

    def get_password_hash(self, password):
        password = password.encode('utf-8')  # Convert string to bytes
        # Generate a salt and hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed_password

    def verify_password(self, plain_password, hashed_password):
        plain_password = plain_password.encode('utf-8')
        # hashed_password should come from your database or storage
        hashed_password = hashed_password.encode('utf-8')
        if bcrypt.checkpw(plain_password, hashed_password):
            return True
        else:
            return False

    def encode_token(self, user):
        payload = {
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=1, minutes=0),
            'iat': datetime.now(tz=timezone.utc),
            "id": str(user.id),
            "email": user.email
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
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
