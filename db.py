import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('contact.db')
        self.db = self.con.cursor()

    def init(self):
        """initalize database and tables if not created"""

        pass
