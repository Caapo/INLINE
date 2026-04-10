FROM python:3.12-slim

LABEL maintainer="INLINE Project"
LABEL description="INLINE — Application de gestion quotidienne"

# Répertoire de travail
WORKDIR /app

# Copie des dépendances
COPY requirements.txt .

# Installation des dépendances
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libdbus-1-3 \
    libxcb-xinerama0 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY src/ ./src/
COPY tests/ ./tests/

# Variable d'environnement pour Qt en mode offscreen
ENV QT_QPA_PLATFORM=offscreen
ENV PYTHONPATH=/app/src

# Commande par défaut : lancer les tests
CMD ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]