import sqlite3


class DB:
    def __init__(self):
        self.con = sqlite3.connect('contact.db')
        self.db = self.con.cursor()

    def init(self):
        """initalize database and tables if not created"""

        self.db.execute(
            """CREATE TABLE user (
                id integer PRIMARY KEY,
                record_created text,
                last_logged_in text,
                username text,
                password text
            )""")

        self.db.execute(
            """CREATE TABLE contact (
                id integer PRIMARY KEY,
                first_name text,
                last_name text,
                email text,
                phone text,
                record_created text,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )""")
        
        self.con.commit()

    def new_user(self, name: str, password: str):
        """add a new user to the database"""

        self.db.execute(
            """INSERT INTO user VALUES (
                datetime('now'),
                datetime('now'),
                name,
                password
            )""")

        self.con.commit()

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
