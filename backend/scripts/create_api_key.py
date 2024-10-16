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
    # TODO: later on, generate the api key from a front call
    # key = str(uuid.uuid4()).replace("-", "")
    key = input("Enter a value for the api key: ")

    data_path = os.path.join(os.path.dirname(__file__), "../data")
    conn = sqlite3.connect(os.path.join(data_path, 'messages.db'))

    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO api_keys (key) VALUES ('{key}')
    ''')

    conn.commit()
    print(f"The API key is: {key}")


if __name__ == '__main__':
    main()

