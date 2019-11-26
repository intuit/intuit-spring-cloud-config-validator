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

if [ "${ACTION}" == "package" ]; then
  echo "${green}* Packaging the Github Enterprise artifact for upload"

elif  [ "${ACTION}" == "pull" ]; then
  echo "${green}* Pulling the Github Enterprise artifact from Docker Hub"

else
  echo "${red}ERROR: set ACTION=package | pull in file '.env'"
fi
echo "${green}* File will be: ${yellow}intuit-spring-cloud-config-validator-${VERSION}.tar.gz"

echo ""
echo "${red}==========--------- Building the new docker image -----------=========="
echo ""
echo "${green}* docker-compose build${yellow}"
echo ""

if [ "${ACTION}" == "package" ]; then
  docker-compose build

elif  [ "${ACTION}" == "pull" ]; then
  docker-compose pull
fi

echo ""
DOCKER_IMAGE=intuit/intuit-spring-cloud-config-validator:${VERSION}

echo "${red}==========--------- Tagging Image -----------=========="
echo ""
echo "${green}* docker tag ${DOCKER_IMAGE} pre-receive.spring-config-validator${yellow}"
echo ""

docker tag ${DOCKER_IMAGE} pre-receive.spring-config-validator

echo ""
echo "${red}==========--------- Create a container -----------=========="
echo ""
echo "${green}* docker create --name config-validator ${DOCKER_IMAGE} /bin/true${yellow}"
echo ""

docker create --name config-validator ${DOCKER_IMAGE} /bin/true

echo ""
echo "${red}==========--------- Export .tar.gz -----------=========="
echo ""
echo "${green}* docker export config-validator | gzip > intuit-spring-cloud-config-validator-${VERSION}.tar.gz${yellow}"
echo ""

docker export config-validator | gzip > intuit-spring-cloud-config-validator-${VERSION}.tar.gz

echo ""
echo "${red}==========--------- Clean up -----------=========="
echo ""
echo "${green}* docker stop config-validator && docker rm config-validator && ls -la intuit-spring-cloud-config-validator-${VERSION}.tar.gz${yellow}"
echo ""
docker stop config-validator && docker rm config-validator && ls -la intuit-spring-cloud-config-validator-${VERSION}.tar.gz
echo ""

echo "${red}==========--------- Upload to Github Enterprise -----------=========="
echo "${yellow}"

date

echo ""
echo "${green}You can now install version '${VERSION}' on your Github Enterprise installation"
echo "${green}* File to upload: ${yellow}$(pwd)/intuit-spring-cloud-config-validator-${VERSION}.tar.gz"
echo ""
echo "${green}* Your users can now enable this ${yellow}Pre-receive hook${green} on a github repo to verify it"
echo ""
