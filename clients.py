from db import DB
from middleware.auth import Auth

db = DB()
auth = Auth()

db.setup(auth)
auth.setup(db)
