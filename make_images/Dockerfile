# Utilisez une image Python officielle comme image de base
FROM python:3.8-slim-buster

# Définissez le répertoire de travail dans le conteneur
WORKDIR /make_images

# Copiez les fichiers de dépendances et installez les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiez les fichiers nécessaires dans le conteneur
COPY . .

# Définissez la commande pour exécuter votre script Python
CMD ["python", "make_images.py"]