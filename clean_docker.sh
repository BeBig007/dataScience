#!/bin/bash

# Arrêter tous les conteneurs
docker stop $(docker ps -q)

# Supprimer tous les conteneurs
docker rm $(docker ps -a -q)

# Supprimer tous les volumes
docker volume rm $(docker volume ls -q)

# Supprimer toutes les images
docker rmi $(docker images -q)

# Supprimer tous les réseaux personnalisés
docker network rm $(docker network ls -q)

echo "~> Full clean docker done!"
