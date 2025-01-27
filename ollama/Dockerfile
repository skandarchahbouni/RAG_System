FROM ollama/ollama
RUN apt-get update && apt-get install -y curl

# Ajout d'un script d'entrée pour démarrer le service et télécharger les modèles à l'exécution
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
