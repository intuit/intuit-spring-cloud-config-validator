FROM github-enterprise-pre-receive-hook-base
MAINTAINER Marcello_deSales@intuit.com

RUN \
  apk add --no-cache py-pip && \
  pip install yamllint pyyaml pyjavaproperties

ADD ./validate_config_files.py /home/git/test.git/hooks/pre-receive
