import sqlite3
import bcrypt

# Définir le chemin de la base de données SQLite
db_path = 'messages.db'

# Fonction pour hasher un mot de passe
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Créer un nouvel utilisateur
def create_user(email: str, password: str):
    hashed_password = hash_password(password)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ajouter l'utilisateur à la table 'users'
    cursor.execute('''
        INSERT INTO users (email, password)
        VALUES (?, ?)
    ''', (email, hashed_password))
    
    conn.commit()
    conn.close()
    print(f"Utilisateur {email} créé avec succès.")

# Exemple d'utilisation
if __name__ == "__main__":
    create_user("test@example.com", "password")
