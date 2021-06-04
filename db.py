import json
from models.models import Contact
import mysql.connector
from datetime import datetime
from middleware.hash import hash_password


class DB:
    def __init__(self):
        with open('secrets.json') as f:
            secrets = json.loads(f.read())

        self.con = mysql.connector.connect(
            host=secrets['DB_HOST'],
            database=secrets['DB_DB'],
            user=secrets['DB_USER'],
            password=secrets['DB_PASS']
        )
        self.db = self.con.cursor()
        self.auth = None
        self.init()

    def setup(self, auth):
        self.auth = auth

    def init(self):
        """initalize database and tables if not created"""

        self.db.execute('''CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            record_created VARCHAR(255) NOT NULL,
            last_logged_in VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )''')

        self.db.execute('''CREATE TABLE IF NOT EXISTS contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(255) NOT NULL UNIQUE,
            record_created VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )''')

        self.con.commit()

    def new_user(self, user: dict) -> tuple:
        """add a new user to the database"""

        time = str(datetime.utcnow())

        try:
            self.db.execute('''INSERT INTO user
                (record_created, last_logged_in, username, password)
                VALUES (%s, %s, %s, %s)''',
                (time, time, user['username'], hash_password(user['password'], user['username']))
            )
            self.con.commit()
            return (0, None)
        except mysql.connector.Error as e:
            if e.errno == 1062: return (409, 'Username already exists')
            else: return (500, e)

    def new_contact(self, id: int, contact: Contact) -> tuple:
        """create a new contact for the user"""

        time = str(datetime.utcnow())

        try:
            self.db.execute('''INSERT INTO contact
                (first_name, last_name, email, phone, record_created, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)''',
                (contact.first_name, contact.last_name, contact.email, contact.phone,
                time, id)
            )
            self.con.commit()
            return (0, None)
        except mysql.connector.Error as e:
            if e.errno == 1062: return (409, 'Contact already exists')
            else: return (500, e)

    def del_contact(self, id: int, contact: Contact) -> tuple:
        """delete contact for the user"""

        try:
            self.db.execute('''DELETE FROM contact
                WHERE user_id = %s AND email = %s''',
                (id, contact.email))
            self.con.commit()
            return (0, None)
        except mysql.connector.Error as e:
            return (500, e)

    def get_contacts(self, id: int) -> tuple:
        """return a list of contacts for the user"""

        try:
            self.db.execute(''' SELECT * FROM contact
                WHERE user_id = %s''', (id,)
            )
            contacts = self.db.fetchall()
            return (contacts, 0, None)
        except mysql.connector.Error as e:
            return (None, 500, e)

    def get_user(self, username: str, password: str) -> tuple:
        """return user and error"""

        try:
            self.db.execute('''SELECT * FROM user
                WHERE username = %s AND password = %s''',
                (username, hash_password(password, username)))

            user = self.db.fetchone()
            if not user: return (None, None, 401, 'Unauthorized')

            user = {
                'id' : user[0],
                'record_created' : user[1],
                'last_logged_in' : user[2],
                'username' : user[3],
                'password' : user[4]
            }

            return (user, self.auth.encode_token(user['id']), 0, None)
        except mysql.connector.Error as e:
            return (None, None, 500, e)

    def lookup_user(self, id: int) -> tuple:
        """return user for decode_token function"""

        try:
            self.db.execute('SELECT * FROM user WHERE id = %s', (id,))

            user = self.db.fetchone()
            if not user: return (None, 401, 'Unauthorized')

            user = {
                'id' : user[0],
                'record_created' : user[1],
                'last_logged_in' : user[2],
                'username' : user[3],
                'password' : user[4]
            }

            return (user, 0, None)
        except mysql.connector.Error as e:
            return (None, 500, e)

    def update_user_activity(self, id: int) -> tuple:
        """update user last_logged_in time"""

        time = str(datetime.utcnow())

        try:
            self.db.execute('''UPDATE user
                SET last_logged_in = %s WHERE id = %s''', (time, id))
            self.con.commit()
            return (0, None)
        except mysql.connector.Error as e:
            return (500, e)

    def update_contact(self, id: int, contact_id: str, contact: Contact) -> tuple:
        """update contact where id is user id and contact_id is the contact's
        id with the new contact dict payload"""

        try:
            self.db.execute('''UPDATE contact SET first_name=%s, last_name=%s,
                email=%s, phone=%s WHERE user_id=%s AND id=%s''',
            (contact.first_name, contact.last_name, contact.email, contact.phone,
             id, contact_id)
            )

            self.con.commit()
            return (0, None)
        except mysql.connector.Error as e:
            return (500, e)

    def search(self, id: int, search: str) -> tuple:
        """return a list of contacts that have a partial match to the search
        string"""

        try:
            self.db.execute('''SELECT * FROM contact
                WHERE user_id=%s AND (first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
                OR phone LIKE %s)''',
                (id, f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'))
            return (self.db.fetchall(), 0, None)
        except mysql.connector.Error as e:
            return (None, 500, e)
