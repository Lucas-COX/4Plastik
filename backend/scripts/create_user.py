import bcrypt
import os
import sqlite3
import uuid

# Hash a password using bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def main():
    # Ask user for email, /!\ this is not double checked for now
    email = input("Insert user email: ")
    password = str(uuid.uuid4()).split('-')[-1]

    data_path = os.path.join(os.path.dirname(__file__), "../data")
    conn = sqlite3.connect(os.path.join(data_path, 'messages.db'))

    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO users (email, password) VALUES ('{email}', '{hash_password(password)}')
    ''')

    conn.commit()
    # TODO: this mush be removed in order to directly send the password by email
    print(f"The user's password is: {password}")


if __name__ == '__main__':
    main()

