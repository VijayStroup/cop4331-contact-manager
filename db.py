import sqlite3
from datetime import datetime

class DB:
    def __init__(self):
        self.con = sqlite3.connect('contact.db', check_same_thread=False)
        self.db = self.con.cursor()

    def init(self):
        """initalize database and tables if not created"""

        self.db.execute(
            '''CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_created TEXT NOT NULL,
                last_logged_in TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )''')

        self.db.execute(
            '''CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                record_created TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )''')
        
        self.con.commit()
        
    def new_user(self, name: str, password: str) -> tuple:
        """add a new user to the database"""
        
        time = str(datetime.utcnow())
        
        try:
            self.db.execute('''INSERT INTO user
                            (record_created, last_logged_in, username, password)
                            VALUES (?, ?, ?, ?)''',
                            (time, time, name, password))

            self.con.commit()
            return (0, None)
        except sqlite3.Error as e:
            if type(e.__class__) == type(sqlite3.IntegrityError):
                return (1, 'Username already exists')
            else:
                print(e, e.__class__)
                return (2, e)

    def new_contact(self, id: str, name: str):
        """create a new contact for the user"""

        pass

    def del_contact(self, id: str, name: str):
        """delete contact for the user"""

        pass

    def get_contacts(self, id: str):
        """return a list of contacts for the user"""

        pass


db = DB()
