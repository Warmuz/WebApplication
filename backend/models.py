from pony.orm import Database, Required, Optional, PrimaryKey, db_session, select
from werkzeug.security import generate_password_hash, check_password_hash
from ulid import ULID
from enum import Enum

ULID_LEN = 26

db = Database()

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class User(db.Entity):
    id = PrimaryKey(str, ULID_LEN, default = lambda: str(ULID()))
    username = Required(str, unique = True)
    password = Required(str)
    role = Required(str, default=Role.USER.value)
    file = Optional('File')

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class File(db.Entity):
    id = PrimaryKey(str, ULID_LEN, default = lambda: str(ULID()))
    filename = Required(str)
    path = Required(str)
    user = Required(User, unique = True)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def add_user(username, password, role=Role.USER.value):
    # Check if the user already exists
    if User.get(username=username):
        print(f"User '{username}' already exists.")
        return None

    # Create a new user and hash the password
    user = User(
        username=username,
        password=generate_password_hash(password),
        role=role
    )

    print(f"User '{username}' added successfully with role '{role}'")
    return user

@db_session
def print_all_users():
    users = select(u for u in User)[:]
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}, Role: {user.role}")

if __name__ == '__main__':
    # Example usage to add a user
    # add_user(username="mati", password="pass", role="admin")
    # add_user(username="test", password="test", role="user")
    print_all_users()