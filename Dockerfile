####### Build Image

FROM marcellodesales/github-enterprise-prereceive-hook-base as tests

# Install dependencies
RUN apk add --no-cache py-pip && \
    pip install coverage

# Make a cache-eligible dependencies
COPY requirements.txt /build/requirements.txt

# Install dependencies
RUN pip install -r /build/requirements.txt

# Copy resources
COPY ./tests /build/tests
COPY ./validate_config_files.py /build

RUN coverage run -m unittest discover -v /build/tests

###### Runtime Image

FROM marcellodesales/github-enterprise-prereceive-hook-base as runtime

RUN apk add --no-cache py-pip

COPY --from=tests /build/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --from=tests /build/validate_config_files.py /home/git/test.git/hooks/pre-receive
