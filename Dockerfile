####### Build Image

FROM marcellodesales/git-pre-receive-hook:python3 as tests

# Make a cache-eligible dependencies
COPY requirements-tests.txt /build/requirements.txt

# Install dependencies
RUN pip install -r /build/requirements.txt

# Copy resources
COPY ./tests /build/tests
COPY ./validate_config_files.py /build

# Glob2 warnings https://github.com/miracle2k/python-glob2/issues/24
ENV PYTHONWARNINGS="ignore::DeprecationWarning:glob2"

RUN coverage run -m unittest discover -v /build/tests

###### Runtime Image

FROM marcellodesales/git-pre-receive-hook:python3 as runtime

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --from=tests /build/validate_config_files.py /home/git/test.git/hooks/pre-receive

# Glob2 warnings https://github.com/miracle2k/python-glob2/issues/24
ENV PYTHONWARNINGS="ignore::DeprecationWarning:glob2"
