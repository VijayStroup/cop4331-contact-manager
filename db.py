import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('contact.db')
        self.db = self.con.cursor()

    def init(self):
        """initalize database and tables if not created"""

        pass

    def new_user(self, name: str, password: str):
        """add a new user to the database"""

        pass

    def new_contact(self, id: str, name: str):
        """create a new contact for the user"""

        pass

    def del_contact(self, id: str, name: str):
        """delete contact for the user"""

        pass

    def get_contacts(self, id: str):
        """return a list of contacts for the user"""

        pass
