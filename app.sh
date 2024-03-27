#!/bin/bash

docker_compose="docker-compose -f docker-compose.yml"

[ -f .env ] || { echo "Missing .env file. Exiting."; exit 1; }

if [[ $1 = "start" ]]; then
  echo "Starting Pelorus Past Due API..."
	$docker_compose up -d
elif [[ $1 = "stop" ]]; then
	echo "Stopping Pelorus Past Due API..."
	$docker_compose stop
elif [[ $1 = "restart" ]]; then
	echo "Restarting Pelorus Past Due API..."
  $docker_compose down
  $docker_compose start
elif [[ $1 = "down" ]]; then
	echo "Tearing Down Pelorus Past Due API..."
	$docker_compose down
elif [[ $1 = "rebuild" ]]; then
	echo "Rebuilding Pelorus Past Due API..."
	$docker_compose down --remove-orphans
	$docker_compose build --no-cache
elif [[ $1 = "shell" ]]; then
	echo "Entering Pelorus Past Due API Shell..."
	docker exec -it pelorus-pastdue sh
else
	echo "Unkown or missing command..."
fi