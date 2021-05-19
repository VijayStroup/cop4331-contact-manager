from datetime import datetime, timedelta
import jwt
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
            # check user in db
            user = None
            if not user:
                raise HTTPException(status_code=404, detail='User not found')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=500, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')
        
        # update last logged in

        return user[0] # return user id from db

    def verify(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """wrapper function for routes"""

        return self.decode_token(auth.credentials)
