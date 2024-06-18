# Utilisez une image de base Python
FROM python:3.8-slim-buster

# Définissez un répertoire de travail
WORKDIR /initialize_db

# Copiez les fichiers de dépendances et installez les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers de l'application
COPY . .

# Exécutez le script Python lorsque le conteneur Docker est lancé
CMD ["python", "initialize_db.py"]