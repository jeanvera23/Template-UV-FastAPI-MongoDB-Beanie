import jwt
from datetime import datetime, timezone, timedelta

payload = {
    'exp': datetime.now(tz=timezone.utc) + timedelta(days=1, minutes=0),
    'iat': datetime.now(tz=timezone.utc),
    'sub': {
        "id": "23213",
        "email": "email"
    }
}

encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")
print(encoded_jwt)
token = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
print(token)