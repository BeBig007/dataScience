#!/bin/bash

# stop all containers
docker stop $(docker ps -q)

# remove all containers
docker rm $(docker ps -a -q)

# remove volumes
docker volume rm $(docker volume ls -q)

# remove images
docker rmi $(docker images -q)

# remove networks
docker network rm $(docker network ls -q)

# remove all images
docker system prune -a

echo ""
echo "~> Full clean docker done!"
