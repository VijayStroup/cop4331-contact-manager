from datetime import datetime, timedelta
import jwt
from db import db
from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class Auth:
    security = HTTPBearer()

    def __init__(self):
        self.secret = 'secret'

    def encode_token(self, id: str):
        """return encoded jwt token after logging in"""

        return jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
            'id': id
            },
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        """decode jwt token and return user id from db if valid"""

        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            user, error, message = db.get_user(payload['id'])
            if not user: raise HTTPException(status_code=error, detail=message)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=500, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

        db.update_user_activity(payload['id'])

        return user

    def verify(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """wrapper function for routes"""

        return self.decode_token(auth.credentials)


auth = Auth()
