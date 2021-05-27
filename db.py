import sqlite3
from datetime import datetime
from middleware.hash import hash_password
from middleware.auth import auth


class DB:
    def __init__(self):
        self.con = sqlite3.connect('contact.db', check_same_thread=False)
        self.db = self.con.cursor()

    def init(self):
        """initalize database and tables if not created"""

        self.db.execute('''CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_created TEXT NOT NULL,
            last_logged_in TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')

        self.db.execute('''CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            record_created TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )''')

        self.con.commit()


    def new_user(self, user: dict) -> tuple:
        """add a new user to the database"""

        time = str(datetime.utcnow())

        try:
            self.db.execute('''INSERT INTO user
                (record_created, last_logged_in, username, password)
                VALUES (?, ?, ?, ?)''',
                (time, time, user['username'], hash_password(user['password'], user['username']))
            )
            self.con.commit()
            return (0, None)
        except sqlite3.Error as e:
            if type(e.__class__) == type(sqlite3.IntegrityError):
                return (409, 'Username already exists')
            else: return (500, e)


    def new_contact(self, id: int, contact: dict) -> tuple:
        """create a new contact for the user"""

        pass


    def del_contact(self, id: int, contact: dict) -> tuple:
        """delete contact for the user"""

        pass


    def get_contacts(self, id: int) -> tuple:
        """return a list of contacts for the user"""

        pass


    def get_user(self, username: str, password: str) -> tuple:
        """return user and error"""
        
        try:
            self.db.execute('''SELECT * FROM user
                WHERE username = ? AND password = ?''',
                username, hash_password(password, username))

            user = self.db.fetchone()

            user = {
                'id' : user[0],
                'record_created' : user[1],
                'last_logged_in' : user[2],
                'username' : user[3],
                'password' : user[4]
            }

            if not user: return (None, None, 401, 'Unauthorized')
            else: return (user, auth.encode_token(user['id']), 0, None)
        except sqlite3.Error as e:
            return (None, None, 500, e)


    def update_user_activity(self, id: int) -> tuple:
        """update user last_logged_in time"""

        time = str(datetime.utcnow())

        try:
            self.db.execute('''UPDATE user
                SET last_logged_in = ? WHERE id = ?''', time, id)
            self.con.commit()

            self.db.execute('SELECT * FROM user WHERE id = ?', id)
            return (self.db.fetchone(), 0, None)
        except sqlite3.Error as e:
            return (None, 500, e)


    def update_contact(self, id: int, contact_id: int, contact: dict) -> tuple:
        """update contact where id is user id and contact_id is the contact's
        id with the new contact dict payload"""

        pass


    def search(self, id: int, search: str) -> tuple:
        """return a list of contacts that have a partial match to the search
        string"""

        try:
            self.db.execute('''SELECT * FROM user
                WHERE id = ? AND * LIKE %?%''', id, search)
            self.con.commit()
            return (self.db.fetchall(), 0, None)
        except sqlite3.Error as e:
            return (self.db.fetchall(), 500, e)


db = DB()
