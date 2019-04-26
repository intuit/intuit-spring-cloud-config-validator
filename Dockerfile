####### Build Image

FROM marcellodesales/github-enterprise-prereceive-hook-base as tests

RUN apk add --no-cache py-pip
COPY requirements.txt requirements.txt
RUN pip2 install -r requirements.txt && \
    pip2 install coverage

ADD . /build
WORKDIR /build

RUN coverage run -m unittest discover -v tests

###### Runtime Image

FROM marcellodesales/github-enterprise-prereceive-hook-base as runtime

RUN apk add --no-cache py-pip

COPY --from=tests /build/requirements.txt requirements.txt
RUN pip2 install -r requirements.txt

COPY --from=tests /build/validate_config_files.py /home/git/test.git/hooks/pre-receive
