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
echo "${red}##### INTUIT SPRING CLOUD CONFIG VALIDATOR #####${yellow}"
echo ""
date
echo ""
echo "${green}* Executing the validations in local Github repo"
echo ""

echo "${red}==========--------- Github Config Repo -----------=========="
echo ""

echo "${green}* Current Dir: ${yellow}$(pwd)"
echo ""
ls -la
echo ""

echo "${red}==========--------- Setting Test Remote Origin -----------=========="
echo ""

echo "${green}* Adding the git origin to current directory with server at ${yellow}$(ipconfig getifaddr en0)"
echo ""
git remote remove test || true
git remote add test git@$(ipconfig getifaddr en0):test.git

echo "${red}==========--------- Testing Remote Origin -----------=========="
echo ""

echo "${green}* Conectivity with the repo..."
echo "${yellow}GIT_SSH_COMMAND=\"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ${GITHUB_SIMULATOR_SSH_PATH}\" git remote show test"
echo ""
GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ${GITHUB_SIMULATOR_SSH_PATH}" git remote show test
echo ""

echo "${red}==========--------- Testing Remote Origin -----------=========="
echo ""
echo "${green}* Executing 'git push' to test github simulator"
echo "${yellow}GIT_SSH_COMMAND=\"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ${GITHUB_SIMULATOR_SSH_PATH}\" git push -u test master"
GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ${GITHUB_SIMULATOR_SSH_PATH}" git push -u test master
echo ""

#echo "${green}* Copy the current validator script to the data container"
#echo "${yellow}docker cp ../validate_config_files.py data:/home/git/test.git/hooks/pre-receive

if [ ! -z "${BRANCH}" ]; then
  echo ""
  echo "${green}* Testing additional branch ${yellow}${BRANCH}"
  echo "GIT_SSH_COMMAND=\"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ${GITHUB_SIMULATOR_SSH_PATH}\" git push test ${BRANCH} -f"
  GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ${GITHUB_SIMULATOR_SSH_PATH}" git push test ${BRANCH} -f
fi
