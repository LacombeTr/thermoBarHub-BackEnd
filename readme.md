# Python Backend avec FastAPI, Docker et Uvicorn

Ce projet est une API backend légère construite avec**FastAPI**. Elle utilise Docker pour faciliter l’installation et l’exécution dans un environnement isolé. Ce guide vous expliquera comment configurer et lancer l'application, même si vous n'avez jamais utilisé Docker auparavant.

## Fonctionnalités

- **Technologies utilisées**:
    - `Python 3.13.0`
    - `FastAPI` pour créer l'API
    - `Uvicorn` pour le serveur web ASGI
    - `Thermobar` pour les calculs
    - Bibliothèques supplémentaires :`Pandas`,`Numpy`, `Pydantic`
- **Support pour le développement interactif**: Les modifications dans les fichiers Python sont visibles immédiatement grâce à Docker et au rechargement automatique.

---

## Pré-requis

Avant de commencer, assurez-vous que votre système est configuré avec :

1. **Docker**: Installez Docker Desktop.
    - [Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop/)
    - Une fois installé, assurez-vous que Docker fonctionne correctement en exécutant la commande suivante dans votre terminal :

      ``` bash
      docker --version
      ```

      Vous devriez voir la version de Docker affichée.
   

2. **Docker Compose**: Docker Desktop inclut Docker Compose. Vérifiez qu'il est disponible :

    ```bash
    docker-compose --version
    ```


---

## I. Installation et lancement de l'application

### Étape 1 : Cloner le projet

Clonez ce dépôt sur votre machine locale :

``` bash
git clone https://github.com/votre-utilisateur/python-backend-docker.git
cd python-backend-docker
```

### Étape 2 : Construction de l'image Docker

Construisez l'image Docker (nécessaire uniquement la première fois ou après des modifications dans le fichier`Dockerfile`) :

```bash
docker-compose build
```

### Étape 3 : Lancer l'application

Démarrez le conteneur avec Docker Compose :

```bash
docker-compose up
```

- Si tout se passe bien, vous devriez voir des logs indiquant que le serveur **Uvicorn** est en cours d'exécution.
- Accédez à votre API via votre navigateur en utilisant une application Front-End ou un outil comme `curl` ou **Postman**:
    - http://localhost:8000: Point d'entrée principal
    - http://localhost:8000/docs: Documentation interactive Swagger de l'API.

---

## II. Structure du Projet

```perl
my-python-backend/ 

├── app/                 # Dossier contenant les fichiers Python
│   ├── main.py          # Point d'entrée principal de l'application
├── requirements.txt     # Liste des dépendances Python
├── Dockerfile           # Instructions pour construire l'image Docker
├── docker-compose.yml   # Configuration pour orchestrer le conteneur Docker
```

### Explication des Fichiers Importants

- **`Dockerfile`**: Définit l’environnement de base, installe Python et configure les dépendances nécessaires pour le projet.
- **`docker-compose.yml`**: Simplifie le lancement de l'application en définissant les ports, les volumes, et les options de démarrage.
- **`app/main.py`**: Contient le code Python de votre application. Vous pouvez modifier ce fichier pour ajouter de nouvelles fonctionnalités.

---

## III. Développement Interactif

Le projet est configuré pour permettre un développement interactif grâce au montage de volumes Docker :

- Les modifications dans les fichiers du dossier`app`sont immédiatement visibles dans le conteneur.
- Le serveur**Uvicorn**redémarre automatiquement avec l'option`--reload`.

---

## IV. Commandes Utiles

### Arrêter l'application

Appuyez sur`CTRL+C`dans votre terminal ou exécutez :

```bash
docker-compose down
```

### Supprimer les conteneurs et nettoyer les images

```bash
docker-compose down --rmi all --volumes --remove-orphans
```

### Vérifier les logs en direct

```bash
docker-compose logs -f
```

### Recréer et redémarrer le conteneur (si des modifications sont apportées)

```bash
docker-compose up --build
```

---

## V. Résolution rapide des problèmes

### Docker n'est pas reconnu dans le terminal

Assurez-vous que Docker Desktop est installé et en cours d’exécution.

### Le port 8000 est déjà utilisé

Un autre processus peut utiliser ce port. Changez le port dans`docker-compose.yml`:

```
ports:   - "8080:8000" 
```

Accédez ensuite à http://localhost:8080.

---

## Aller Plus Loin

- **Tests unitaires**: Intégrez`pytest`pour tester vos fonctions Python.