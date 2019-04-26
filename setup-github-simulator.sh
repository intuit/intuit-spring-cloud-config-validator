#!/usr/bin/env bash

# Colors
green=`tput setaf 2`
red=`tput setaf 1`
yellow=`tput setaf 3`
blue=`tput setaf 4`
reset=`tput sgr0`
CURRENT_SCRIPT=$(basename "$0")

source .env

echo ""
echo "${red}##### INTUIT SPRING CLOUD CONFIG VALIDATOR ${VERSION} #####${yellow}"
echo ""
date
echo ""
echo "${green}* Setting up a Github Server simulator"
echo ""

echo "${red}==========--------- Building the new docker image -----------=========="
echo ""
echo "${green}* docker-compose build${yellow}"
echo ""
docker-compose build
echo ""

DOCKER_IMAGE=intuit/intuit-spring-cloud-config-validator:${VERSION}

echo "${red}==========--------- Start the data container -----------=========="
echo ""
echo "${green}* docker run --name data ${DOCKER_IMAGE} /bin/true${yellow}"
echo ""
docker stop data || true
docker rm data || true
docker run --name data ${DOCKER_IMAGE} /bin/true
#echo "Copy the current validator script to the data container If needed for testing without rebuilding
#docker cp validate_config_files.py data:/home/git/test.git/hooks/pre-receive
echo ""

echo "${red}==========--------- Start a new Github Server simulator -----------=========="
echo ""
echo "${green}* docker run --name gitrepo -e GITHUB_PULL_REQUEST_HEAD=00000000 -e GITHUB_PULL_REQUEST_BASE=f394274 -d -p 52311:22 --volumes-from data -e GIT_DIR=/home/git/test.git ${DOCKER_IMAGE}${yellow}"
echo ""
docker stop gitrepo || true
docker rm gitrepo || true
docker run --name gitrepo -e GITHUB_PULL_REQUEST_HEAD=00000000 -e GITHUB_PULL_REQUEST_BASE=f394274 -d -p 52311:22 --volumes-from data -e GIT_DIR=/home/git/test.git ${DOCKER_IMAGE}
echo ""

SIMULATOR_SSH_PEM=$(pwd)/.id_rsa_from_github_simulator_server

echo "${red}==========--------- Copying credentials from Github server Container -----------=========="
echo ""
echo "${green}* docker cp data:/home/git/.ssh/id_rsa ${SIMULATOR_SSH_PEM}${yellow}"
echo ""
docker cp data:/home/git/.ssh/id_rsa ${SIMULATOR_SSH_PEM}
echo ""

date
echo "${green}"
echo "* Finished setting up the server..."
echo "* Now you can run tests with test.sh copying the command below:"
echo ""
echo "${yellow}GITHUB_SIMULATOR_SSH_PATH=${SIMULATOR_SSH_PEM} ./test.sh"
echo ""
