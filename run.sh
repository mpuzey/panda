#!/bin/bash
#set -e

function db() {
    docker pull mongodb/mongodb-community-server:latest
    docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
    python3 -m  src.db.seed
}

function app() {
    docker build . -t panda
    docker rm -f panda
    docker run -it -p 8888:8888 --name panda panda
}

function clearAllContainers() {
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
}

function all() {
  app
  db
}

$@