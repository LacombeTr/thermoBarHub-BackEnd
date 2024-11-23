# Utiliser l'image Python officielle
FROM python:3.13-slim

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier les scripts
COPY ./app ./app

# Exposer le port pour FastAPI
EXPOSE 8000

# Lancer le serveur Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Executer les tests
#(déconseillé) Décommenter si et seulement si l'on souhaite ne pas faire les tests manuellement
# CMD ["pytest", "tests/"]
