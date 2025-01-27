#!/bin/bash
# Lancer le serveur ollama
nohup ollama serve &

# Attendre que le serveur soit prêt
sleep 5

# Télécharger les modèles
ollama pull gemma:2b
ollama pull nomic-embed-text

# Démarrer le processus principal (par exemple le serveur)
tail -f /dev/null
