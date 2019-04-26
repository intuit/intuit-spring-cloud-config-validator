FROM marcellodesales/github-enterprise-prereceive-hook-base
MAINTAINER Marcello_deSales@intuit.com

RUN apk add --no-cache py-pip

COPY requirements.txt requirements.txt

RUN pip2 install -r requirements.txt

COPY ./validate_config_files.py /home/git/test.git/hooks/pre-receive
