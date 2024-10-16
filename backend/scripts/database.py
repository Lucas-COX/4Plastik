import os
import sqlite3

# Connexion à la base de données (si elle n'existe pas, elle sera créée)
data_path = os.path.join(os.path.dirname(__file__), "../data")
conn = sqlite3.connect(os.path.join(data_path, 'messages.db'))

# Création d'un curseur pour exécuter des commandes SQL
cursor = conn.cursor()

# Création de la table pour stocker les messages traités
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account TEXT NOT NULL,
    content TEXT NOT NULL,
    social TEXT NOT NULL,
    score REAL NOT NULL
)
''')

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()
